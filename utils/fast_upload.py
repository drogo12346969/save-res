# High-Speed Parallel Multi-Connection Upload Accelerator for Pyrogram MTProto.

import asyncio
import functools
import inspect
import io
import logging
import math
import os
import time
from hashlib import md5
from pathlib import PurePath
from typing import Union, BinaryIO, Callable, Optional, List

import pyrogram
from pyrogram import StopTransmission, raw
from pyrogram.session import Session

logger = logging.getLogger(__name__)

# Default concurrency settings (can be overridden via environment)
PARALLEL_SESSIONS_COUNT = int(os.getenv("PARALLEL_MEDIA_SESSIONS", "4"))
UPLOAD_WORKERS_COUNT = int(os.getenv("MAX_CONCURRENT_TRANSMISSIONS", "12"))
QUEUE_BUFFER_SIZE = 32
PART_SIZE = 512 * 1024  # 512 KB (Telegram MTProto optimal part size)

# Cache for multi-connection media sessions per client and DC
# Format: {client_id: {dc_id: [Session, Session, ...]}}
CLIENT_MEDIA_POOLS = {}


async def get_or_create_session_pool(client: "pyrogram.Client", dc_id: int, pool_size: int = PARALLEL_SESSIONS_COUNT) -> List[Session]:
    """
    Creates and maintains a pool of multiple independent MTProto media sessions
    to the target Telegram Datacenter. This bypasses single-TCP connection bandwidth
    and latency bottlenecks, allowing parallel chunk transmission across multiple TCP sockets.
    """
    client_key = getattr(client, "name", id(client))
    if client_key not in CLIENT_MEDIA_POOLS:
        CLIENT_MEDIA_POOLS[client_key] = {}

    pool = CLIENT_MEDIA_POOLS[client_key].get(dc_id)
    if pool and len(pool) >= pool_size:
        # Check that sessions are active
        active_pool = [s for s in pool if getattr(s, "is_connected", True)]
        if len(active_pool) >= pool_size:
            return active_pool

    auth_key = await client.storage.auth_key()
    test_mode = await client.storage.test_mode()

    # Reuse the primary media session as the first session in the pool
    primary_session = client.media_sessions.get(dc_id)
    if not primary_session:
        primary_session = Session(client, dc_id, auth_key, test_mode, is_media=True)
        await primary_session.start()
        client.media_sessions[dc_id] = primary_session

    sessions = [primary_session]

    # Create additional parallel media sessions
    needed = max(0, pool_size - 1)
    for _ in range(needed):
        try:
            extra_session = Session(client, dc_id, auth_key, test_mode, is_media=True)
            await extra_session.start()
            sessions.append(extra_session)
        except Exception as e:
            logger.warning(f"Could not start extra media session: {e}")
            break

    CLIENT_MEDIA_POOLS[client_key][dc_id] = sessions
    logger.info(f"Initialized {len(sessions)} parallel MTProto media sessions for DC {dc_id} on client '{client_key}'")
    return sessions


async def accelerated_save_file(
    self: "pyrogram.Client",
    path: Union[str, BinaryIO],
    file_id: int = None,
    file_part: int = 0,
    progress: Callable = None,
    progress_args: tuple = ()
):
    """
    Ultra-High-Speed multi-connection parallel file uploader for Pyrogram.
    - Pipelined 512KB chunk reading with pre-buffering.
    - Multi-socket parallel MTProto transmission (up to 12-16 workers across 4 TCP connections).
    - Decoupled, non-blocking asynchronous progress dispatch.
    - Automatic part retries on transient network errors.
    """
    async with self.save_file_semaphore:
        if path is None:
            return None

        # Determine file handle and size
        if isinstance(path, (str, PurePath)):
            fp = open(path, "rb")
            should_close = True
        elif isinstance(path, io.IOBase):
            fp = path
            should_close = False
        else:
            raise ValueError("Invalid file. Expected file path string or binary file pointer")

        try:
            file_name = getattr(fp, "name", "file.bin")
            fp.seek(0, os.SEEK_END)
            file_size = fp.tell()
            fp.seek(0)

            if file_size == 0:
                raise ValueError("File size equals 0 B")

            # Check premium file size limits
            if getattr(self, "me", None) and getattr(self.me, "is_premium", False):
                limit_mib = 4000
            else:
                limit_mib = 2000

            if file_size > limit_mib * 1024 * 1024:
                raise ValueError(f"Can't upload files bigger than {limit_mib} MiB")

            part_size = PART_SIZE
            file_total_parts = int(math.ceil(file_size / part_size))
            is_big = file_size > 10 * 1024 * 1024
            is_missing_part = file_id is not None
            file_id = file_id or self.rnd_id()
            md5_sum = md5() if not is_big and not is_missing_part else None

            # Get parallel session pool
            dc_id = await self.storage.dc_id()
            pool_size = PARALLEL_SESSIONS_COUNT if is_big else 2
            sessions = await get_or_create_session_pool(self, dc_id, pool_size=pool_size)

            # Determine worker count
            num_workers = min(UPLOAD_WORKERS_COUNT if is_big else 4, file_total_parts)
            num_workers = max(num_workers, 1)

            queue = asyncio.Queue(maxsize=QUEUE_BUFFER_SIZE)
            uploaded_bytes = 0
            uploaded_lock = asyncio.Lock()
            last_progress_time = 0.0

            async def notify_progress(current_bytes, total_bytes):
                if not progress:
                    return
                try:
                    func = functools.partial(progress, current_bytes, total_bytes, *progress_args)
                    if inspect.iscoroutinefunction(progress):
                        await func()
                    else:
                        await self.loop.run_in_executor(self.executor, func)
                except StopTransmission:
                    raise
                except Exception as e_prog:
                    logger.debug(f"Progress notice: {e_prog}")

            async def worker(worker_idx: int):
                nonlocal uploaded_bytes, last_progress_time
                session = sessions[worker_idx % len(sessions)]
                
                while True:
                    item = await queue.get()
                    if item is None:
                        queue.task_done()
                        return

                    part_num, chunk_bytes = item
                    
                    if is_big:
                        rpc = raw.functions.upload.SaveBigFilePart(
                            file_id=file_id,
                            file_part=part_num,
                            file_total_parts=file_total_parts,
                            bytes=chunk_bytes
                        )
                    else:
                        rpc = raw.functions.upload.SaveFilePart(
                            file_id=file_id,
                            file_part=part_num,
                            bytes=chunk_bytes
                        )

                    # Retry up to 3 times on transient network error
                    success = False
                    for attempt in range(3):
                        try:
                            await session.invoke(rpc)
                            success = True
                            break
                        except StopTransmission:
                            raise
                        except Exception as e_rpc:
                            if attempt == 2:
                                logger.error(f"Part {part_num} upload failed after 3 attempts: {e_rpc}")
                                raise e_rpc
                            # Rotate to another session on retry
                            session = sessions[(worker_idx + attempt + 1) % len(sessions)]
                            await asyncio.sleep(0.5)

                    if success:
                        chunk_len = len(chunk_bytes)
                        async with uploaded_lock:
                            uploaded_bytes += chunk_len
                            curr = uploaded_bytes
                        
                        # Throttle progress execution to avoid event loop stalls
                        now = time.time()
                        if (now - last_progress_time >= 1.0) or (curr >= file_size):
                            last_progress_time = now
                            asyncio.create_task(notify_progress(min(curr, file_size), file_size))

                    queue.task_done()

            # Start worker pool
            workers = [self.loop.create_task(worker(i)) for i in range(num_workers)]

            # Pipelined chunk reader
            try:
                fp.seek(part_size * file_part)
                curr_part = file_part

                while True:
                    chunk = fp.read(part_size)
                    if not chunk:
                        if not is_big and not is_missing_part:
                            md5_sum = "".join([hex(i)[2:].zfill(2) for i in md5_sum.digest()])
                        break

                    if not is_big and not is_missing_part:
                        md5_sum.update(chunk)

                    await queue.put((curr_part, chunk))
                    curr_part += 1

                    if is_missing_part:
                        break

                # Wait for all chunks to finish transmission
                await queue.join()

            except StopTransmission:
                raise
            except Exception as e:
                logger.error(f"Error during accelerated save_file: {e}")
                raise
            finally:
                # Stop workers
                for _ in workers:
                    await queue.put(None)
                await asyncio.gather(*workers, return_exceptions=True)

            # Final progress update to ensure 100% is displayed
            if progress:
                await notify_progress(file_size, file_size)

            if is_big:
                return raw.types.InputFileBig(
                    id=file_id,
                    parts=file_total_parts,
                    name=file_name,
                )
            else:
                return raw.types.InputFile(
                    id=file_id,
                    parts=file_total_parts,
                    name=file_name,
                    md5_checksum=md5_sum
                )

        finally:
            if should_close:
                try:
                    fp.close()
                except Exception:
                    pass


def apply_fast_upload_patch():
    """
    Globally monkey-patches Pyrogram Client.save_file with accelerated_save_file.
    This automatically applies multi-session parallel upload acceleration to:
    send_video, send_document, send_audio, send_photo, send_voice, etc.
    across the entire application.
    """
    try:
        import pyrogram
        pyrogram.Client.save_file = accelerated_save_file
        logger.info("⚡ [Fast Upload Engine] Pyrogram save_file successfully hooked with multi-connection parallel acceleration!")
        print("⚡ [Fast Upload Engine] Pyrogram save_file successfully hooked with multi-connection parallel acceleration!")
        return True
    except Exception as e:
        logger.error(f"Failed to apply fast upload patch: {e}")
        return False
