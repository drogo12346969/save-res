"""
High-Speed Crypto Acceleration Module for Pyrogram and Telethon MTProto.
Ensures native C-accelerated AES encryption/decryption (TgCrypto / OpenSSL)
to prevent fallback to slow pure-Python pyaes (which caps speed at 0.36 MB/s).
"""

import logging
import time

logger = logging.getLogger(__name__)

CRYPTO_ENGINE = "unknown"
CRYPTO_SPEED_MBPS = 0.0


def apply_crypto_optimizations():
    global CRYPTO_ENGINE, CRYPTO_SPEED_MBPS

    # 1. First priority: Native TgCrypto C-extension
    try:
        import tgcrypto
        k = b'k' * 32
        iv = bytearray(b'i' * 16)
        st = bytearray(1)
        data = b'x' * (1024 * 1024)
        t0 = time.time()
        tgcrypto.ctr256_encrypt(data, k, iv, st)
        t1 = time.time()
        dur = t1 - t0
        speed = (1.0 / dur) if dur > 0 else 999.0

        CRYPTO_ENGINE = "TgCrypto (Native C Extension)"
        CRYPTO_SPEED_MBPS = speed
        logger.info(f"⚡ [Crypto Engine] Native {CRYPTO_ENGINE} active! Benchmarked Speed: {speed:.1f} MB/s")
        print(f"⚡ [Crypto Engine] Native {CRYPTO_ENGINE} active! Benchmarked Speed: {speed:.1f} MB/s")
        return True
    except Exception as e_tg:
        logger.warning(f"TgCrypto notice: {e_tg}. Attempting C-acceleration fallback via cryptography OpenSSL...")

    # 2. Fallback priority: OpenSSL C-bindings via cryptography
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms
        import pyrogram.crypto.aes as pyro_aes

        # Benchmark cryptography CTR
        k = b'k' * 32
        iv = b'i' * 16
        data = b'x' * (1024 * 1024)
        t0 = time.time()
        c = Cipher(algorithms.AES(k), modes.CTR(iv))
        enc = c.encryptor()
        enc.update(data)
        t1 = time.time()
        dur = t1 - t0
        speed = (1.0 / dur) if dur > 0 else 999.0

        def fast_xor(a: bytes, b: bytes) -> bytes:
            return int.to_bytes(
                int.from_bytes(a, "big") ^ int.from_bytes(b, "big"),
                len(a),
                "big",
            )

        def fast_ctr256_encrypt(data: bytes, key: bytes, iv: bytearray, state: bytearray = None) -> bytes:
            cipher = Cipher(algorithms.AES(bytes(key)), modes.CTR(bytes(iv)))
            encryptor = cipher.encryptor()
            res = encryptor.update(bytes(data))
            total_blocks = (len(data) + 15) // 16
            iv_int = int.from_bytes(iv, "big") + total_blocks
            iv[:] = (iv_int & ((1 << 128) - 1)).to_bytes(16, "big")
            return res

        def fast_ctr256_decrypt(data: bytes, key: bytes, iv: bytearray, state: bytearray = None) -> bytes:
            return fast_ctr256_encrypt(data, key, iv, state)

        def fast_ige256_encrypt(data: bytes, key: bytes, iv: bytearray) -> bytes:
            cipher = Cipher(algorithms.AES(bytes(key)), modes.ECB())
            encryptor = cipher.encryptor()
            iv1 = iv[:16]
            iv2 = iv[16:]
            out = bytearray(len(data))
            for i in range(0, len(data), 16):
                chunk = data[i:i+16]
                x = fast_xor(chunk, iv1)
                enc = encryptor.update(x)
                res = fast_xor(enc, iv2)
                out[i:i+16] = res
                iv1 = res
                iv2 = chunk
            iv[:16] = iv1
            iv[16:] = iv2
            return bytes(out)

        def fast_ige256_decrypt(data: bytes, key: bytes, iv: bytearray) -> bytes:
            cipher = Cipher(algorithms.AES(bytes(key)), modes.ECB())
            decryptor = cipher.decryptor()
            iv1 = iv[:16]
            iv2 = iv[16:]
            out = bytearray(len(data))
            for i in range(0, len(data), 16):
                chunk = data[i:i+16]
                x = fast_xor(chunk, iv2)
                dec = decryptor.update(x)
                res = fast_xor(dec, iv1)
                out[i:i+16] = res
                iv1 = chunk
                iv2 = res
            iv[:16] = iv1
            iv[16:] = iv2
            return bytes(out)

        # Patch pyrogram.crypto.aes
        pyro_aes.ctr256_encrypt = fast_ctr256_encrypt
        pyro_aes.ctr256_decrypt = fast_ctr256_decrypt
        pyro_aes.ige256_encrypt = fast_ige256_encrypt
        pyro_aes.ige256_decrypt = fast_ige256_decrypt
        pyro_aes.xor = fast_xor

        CRYPTO_ENGINE = "OpenSSL via cryptography (High Speed Patch)"
        CRYPTO_SPEED_MBPS = speed
        logger.info(f"⚡ [Crypto Engine] {CRYPTO_ENGINE} active! Benchmarked Speed: {speed:.1f} MB/s")
        print(f"⚡ [Crypto Engine] {CRYPTO_ENGINE} active! Benchmarked Speed: {speed:.1f} MB/s")
        return True
    except Exception as e_crypto:
        logger.error(f"Failed to apply cryptography patch: {e_crypto}")
        CRYPTO_ENGINE = "Pure Python pyaes (WARNING: Slow ~0.36 MB/s)"
        print(f"⚠️ [Crypto Engine] WARNING: Running on {CRYPTO_ENGINE}! Install gcc and tgcrypto in Dockerfile for full speed.")
        return False


# Automatically invoke upon import
apply_crypto_optimizations()
