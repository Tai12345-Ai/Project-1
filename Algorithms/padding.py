"""
RSA Padding Schemes: OAEP (encryption) and PSS (signature)
Implements PKCS#1 v2.1 standards for secure RSA
"""
from __future__ import annotations
import hashlib
import secrets
from typing import Tuple

from .utilities import bytes_to_int, int_to_bytes


def mgf1(seed: bytes, length: int, hash_func=hashlib.sha256) -> bytes:
    """
    Mask Generation Function based on hash (MGF1 from PKCS#1).
    
    Args:
        seed: Input seed
        length: Desired output length in bytes
        hash_func: Hash function to use (default SHA-256)
        
    Returns:
        Pseudorandom mask of specified length
    """
    hlen = hash_func().digest_size
    if length > (hlen << 32):
        raise ValueError("mask too long")
    
    t = b""
    counter = 0
    while len(t) < length:
        c = counter.to_bytes(4, "big")
        t += hash_func(seed + c).digest()
        counter += 1
    
    return t[:length]


def oaep_encode(message: bytes, n_bits: int, label: bytes = b"", 
                hash_func=hashlib.sha256) -> bytes:
    """
    OAEP encoding (PKCS#1 v2.1, RFC 8017 Section 7.1.1).
    
    Format:
        EM = 0x00 || maskedSeed || maskedDB
        where DB = lHash || PS || 0x01 || M
    
    Args:
        message: Message to encode
        n_bits: RSA modulus bit length
        label: Optional label (usually empty)
        hash_func: Hash function
        
    Returns:
        Encoded message ready for RSA encryption
    """
    hlen = hash_func().digest_size
    k = (n_bits + 7) // 8  # modulus byte length
    mlen = len(message)
    
    # Check message length
    if mlen > k - 2 * hlen - 2:
        raise ValueError("message too long for OAEP encoding")
    
    # 1. Generate lHash = Hash(label)
    lhash = hash_func(label).digest()
    
    # 2. Generate PS (padding string of zeros)
    ps_len = k - mlen - 2 * hlen - 2
    ps = b"\x00" * ps_len
    
    # 3. Construct DB = lHash || PS || 0x01 || M
    db = lhash + ps + b"\x01" + message
    
    # 4. Generate random seed
    seed = secrets.token_bytes(hlen)
    
    # 5. Compute dbMask = MGF(seed, k - hlen - 1)
    db_mask = mgf1(seed, k - hlen - 1, hash_func)
    
    # 6. Compute maskedDB = DB ⊕ dbMask
    masked_db = bytes(a ^ b for a, b in zip(db, db_mask))
    
    # 7. Compute seedMask = MGF(maskedDB, hlen)
    seed_mask = mgf1(masked_db, hlen, hash_func)
    
    # 8. Compute maskedSeed = seed ⊕ seedMask
    masked_seed = bytes(a ^ b for a, b in zip(seed, seed_mask))
    
    # 9. Construct EM = 0x00 || maskedSeed || maskedDB
    em = b"\x00" + masked_seed + masked_db
    
    return em


def oaep_decode(encoded: bytes, n_bits: int, label: bytes = b"",
                hash_func=hashlib.sha256) -> bytes:
    """
    OAEP decoding (PKCS#1 v2.1, RFC 8017 Section 7.1.2).
    
    Args:
        encoded: OAEP-encoded message
        n_bits: RSA modulus bit length
        label: Optional label (must match encoding)
        hash_func: Hash function
        
    Returns:
        Original message
        
    Raises:
        ValueError: If decoding fails (padding error)
    """
    hlen = hash_func().digest_size
    k = (n_bits + 7) // 8
    
    if len(encoded) != k or k < 2 * hlen + 2:
        raise ValueError("decoding error: invalid length")
    
    # 1. Parse EM = Y || maskedSeed || maskedDB
    y = encoded[0]
    masked_seed = encoded[1:1 + hlen]
    masked_db = encoded[1 + hlen:]
    
    # 2. Compute seedMask = MGF(maskedDB, hlen)
    seed_mask = mgf1(masked_db, hlen, hash_func)
    
    # 3. Compute seed = maskedSeed ⊕ seedMask
    seed = bytes(a ^ b for a, b in zip(masked_seed, seed_mask))
    
    # 4. Compute dbMask = MGF(seed, k - hlen - 1)
    db_mask = mgf1(seed, k - hlen - 1, hash_func)
    
    # 5. Compute DB = maskedDB ⊕ dbMask
    db = bytes(a ^ b for a, b in zip(masked_db, db_mask))
    
    # 6. Parse DB = lHash' || PS || 0x01 || M
    lhash = hash_func(label).digest()
    lhash_prime = db[:hlen]
    
    # Find 0x01 separator
    separator_idx = -1
    for i in range(hlen, len(db)):
        if db[i] == 0x01:
            separator_idx = i
            break
        elif db[i] != 0x00:
            raise ValueError("decoding error: invalid padding")
    
    if separator_idx == -1:
        raise ValueError("decoding error: separator not found")
    
    # 7. Check Y and lHash'
    if y != 0x00 or lhash_prime != lhash:
        raise ValueError("decoding error: hash mismatch")
    
    # 8. Extract message
    message = db[separator_idx + 1:]
    return message


def pss_encode(message_hash: bytes, n_bits: int, salt_length: int = None,
               hash_func=hashlib.sha256) -> bytes:
    """
    PSS encoding for signature (PKCS#1 v2.1, RFC 8017 Section 9.1.1).
    
    Format:
        EM = maskedDB || H || 0xbc
        where DB = PS || 0x01 || salt
              H = Hash(padding1 || mHash || salt)
    
    Args:
        message_hash: Hash of message to sign (already computed)
        n_bits: RSA modulus bit length
        salt_length: Salt length in bytes (default = hlen)
        hash_func: Hash function
        
    Returns:
        PSS-encoded signature block
    """
    hlen = hash_func().digest_size
    if salt_length is None:
        salt_length = hlen
    
    emlen = (n_bits + 7) // 8
    
    # Check lengths
    if emlen < hlen + salt_length + 2:
        raise ValueError("encoding error: key too short")
    
    # 1. Generate random salt
    salt = secrets.token_bytes(salt_length)
    
    # 2. Compute M' = (0x)00 00 00 00 00 00 00 00 || mHash || salt
    m_prime = b"\x00" * 8 + message_hash + salt
    
    # 3. Compute H = Hash(M')
    h = hash_func(m_prime).digest()
    
    # 4. Generate PS (padding of zeros)
    ps_len = emlen - salt_length - hlen - 2
    ps = b"\x00" * ps_len
    
    # 5. Construct DB = PS || 0x01 || salt
    db = ps + b"\x01" + salt
    
    # 6. Compute dbMask = MGF(H, emlen - hlen - 1)
    db_mask = mgf1(h, emlen - hlen - 1, hash_func)
    
    # 7. Compute maskedDB = DB ⊕ dbMask
    masked_db = bytes(a ^ b for a, b in zip(db, db_mask))
    
    # 8. Set leftmost bits of maskedDB to zero
    bits_to_zero = 8 * emlen - n_bits
    if bits_to_zero > 0:
        mask = (0xff >> bits_to_zero)
        masked_db = bytes([masked_db[0] & mask]) + masked_db[1:]
    
    # 9. Construct EM = maskedDB || H || 0xbc
    em = masked_db + h + b"\xbc"
    
    return em


def pss_verify(message_hash: bytes, signature_em: bytes, n_bits: int,
               salt_length: int = None, hash_func=hashlib.sha256) -> bool:
    """
    PSS verification (PKCS#1 v2.1, RFC 8017 Section 9.1.2).
    
    Args:
        message_hash: Hash of original message
        signature_em: Decoded signature (after RSA verification)
        n_bits: RSA modulus bit length
        salt_length: Expected salt length (default = hlen)
        hash_func: Hash function
        
    Returns:
        True if signature is valid
    """
    hlen = hash_func().digest_size
    if salt_length is None:
        salt_length = hlen
    
    emlen = (n_bits + 7) // 8
    
    # Check length and trailer
    if len(signature_em) != emlen or signature_em[-1] != 0xbc:
        return False
    
    if emlen < hlen + salt_length + 2:
        return False
    
    # 1. Parse EM = maskedDB || H || 0xbc
    masked_db = signature_em[:emlen - hlen - 1]
    h = signature_em[emlen - hlen - 1:emlen - 1]
    
    # 2. Check leftmost bits
    bits_to_zero = 8 * emlen - n_bits
    if bits_to_zero > 0:
        mask = 0xff >> bits_to_zero
        if masked_db[0] & ~mask:
            return False
    
    # 3. Compute dbMask = MGF(H, emlen - hlen - 1)
    db_mask = mgf1(h, emlen - hlen - 1, hash_func)
    
    # 4. Compute DB = maskedDB ⊕ dbMask
    db = bytes(a ^ b for a, b in zip(masked_db, db_mask))
    
    # 5. Set leftmost bits of DB to zero
    if bits_to_zero > 0:
        db = bytes([db[0] & mask]) + db[1:]
    
    # 6. Check DB format: PS || 0x01 || salt
    ps_len = emlen - hlen - salt_length - 2
    for i in range(ps_len):
        if db[i] != 0x00:
            return False
    
    if db[ps_len] != 0x01:
        return False
    
    # 7. Extract salt
    salt = db[-salt_length:] if salt_length > 0 else b""
    
    # 8. Compute M' = (0x)00 00 00 00 00 00 00 00 || mHash || salt
    m_prime = b"\x00" * 8 + message_hash + salt
    
    # 9. Compute H' = Hash(M')
    h_prime = hash_func(m_prime).digest()
    
    # 10. Compare H and H'
    return h == h_prime
