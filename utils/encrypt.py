# crypto_ops.py
import logging
from cryptography.hazmat.primitives import hashes as hsh
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC as PBK
from cryptography.hazmat.primitives.ciphers import Cipher as Cp, algorithms as alg, modes as md
import base64 as b64
import os as osy
from config import MASTER_KEY as M1, IV_KEY as I1

logger = logging.getLogger(__name__)

DEFAULT_MASTER_KEY = "SaveRestrictedMasterKeySecure2025"
DEFAULT_IV_KEY = "SaveRestrictedIVKey2025"

def dyk(pwd=None, slt=None, l=16):
    pwd_val = (pwd or M1 or DEFAULT_MASTER_KEY).strip()
    slt_val = (slt or I1 or DEFAULT_IV_KEY).strip()
    if not pwd_val:
        pwd_val = DEFAULT_MASTER_KEY
    if not slt_val:
        slt_val = DEFAULT_IV_KEY
    
    pw = pwd_val.encode()
    sl = slt_val.encode()
    kdf = PBK(
        algorithm=hsh.SHA256(),
        length=l,
        salt=sl,
        iterations=100000,
    )
    return kdf.derive(pw)

def ecs(s):
    if not s:
        return ""
    try:
        k = dyk()
        n = osy.urandom(12) 
        cp = Cp(alg.AES(k), md.GCM(n))
        enc = cp.encryptor()
        p = s.encode()
        ct = enc.update(p) + enc.finalize()
        tg = enc.tag
        encd = b64.b64encode(n + tg + ct).decode()
        return encd
    except Exception as e:
        logger.error(f"Error encrypting session: {e}")
        return s

def dcs(ed):
    if not ed:
        return ""
    try:
        k = dyk()
        dat = b64.b64decode(ed.encode())
        if len(dat) < 28:
            # Not an encrypted payload from ecs, return as raw string
            return ed
        n = dat[:12]
        tg = dat[12:28]
        ct = dat[28:]
        cp = Cp(alg.AES(k), md.GCM(n, tg))
        dec = cp.decryptor()
        res = dec.update(ct) + dec.finalize()
        return res.decode()
    except Exception as e:
        logger.debug(f"Decryption notice (handling as raw string session if applicable): {e}")
        # If decryption fails (e.g. raw session string passed without encryption), return raw string
        return ed
