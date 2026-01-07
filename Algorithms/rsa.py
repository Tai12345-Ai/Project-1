from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple
import hashlib

from .utilities import gcd, modinv, modexp, generate_prime, int_to_bytes, bytes_to_int


@dataclass(frozen=True)
class PublicKey:
    e: int
    n: int


@dataclass(frozen=True)
class PrivateKey:
    d: int
    n: int
    # Keep factors for CRT optimization demo
    p: Optional[int] = None
    q: Optional[int] = None
    dp: Optional[int] = None  # d mod (p-1)
    dq: Optional[int] = None  # d mod (q-1)
    qinv: Optional[int] = None  # q^{-1} mod p


def keygen(bits: int = 1024, e: int = 65537, mr_rounds: int = 40) -> Tuple[PublicKey, PrivateKey]:
    """
    Textbook RSA key generation (CLRS 31.7 + 31.8):
    - choose primes p,q
    - n=pq, phi=(p-1)(q-1)
    - choose e with gcd(e,phi)=1
    - d = e^{-1} mod phi
    Also precompute CRT params for demo.
    """
    if bits < 256:
        raise ValueError("bits too small for RSA demo; use >= 256 (512/1024 recommended)")

    p = generate_prime(bits // 2, rounds=mr_rounds)
    q = generate_prime(bits // 2, rounds=mr_rounds)
    while q == p:
        q = generate_prime(bits // 2, rounds=mr_rounds)

    n = p * q
    phi = (p - 1) * (q - 1)

    if gcd(e, phi) != 1:
        e = 3
        while gcd(e, phi) != 1:
            e += 2

    d = modinv(e, phi)

    dp = d % (p - 1)
    dq = d % (q - 1)
    qinv = modinv(q, p)  # q^{-1} mod p (standard CRT form)

    pub = PublicKey(e=e, n=n)
    priv = PrivateKey(d=d, n=n, p=p, q=q, dp=dp, dq=dq, qinv=qinv)
    return pub, priv


class RSA:
    """
    Textbook RSA for learning (no OAEP/PSS):
      encrypt_int: c = m^e mod n
      decrypt_int: m = c^d mod n
    plus basic block encoding and textbook signature on SHA-256 hash.
    """

    def __init__(self, pub: PublicKey, priv: Optional[PrivateKey] = None):
        self.pub = pub
        self.priv = priv

    # ---- core math ----
    def encrypt_int(self, m: int) -> int:
        if not (0 <= m < self.pub.n):
            raise ValueError("m must satisfy 0 <= m < n")
        return modexp(m, self.pub.e, self.pub.n)

    def decrypt_int(self, c: int) -> int:
        if self.priv is None:
            raise ValueError("No private key for decryption")
        if not (0 <= c < self.priv.n):
            raise ValueError("c must satisfy 0 <= c < n")
        return modexp(c, self.priv.d, self.priv.n)

    def decrypt_int_crt(self, c: int) -> int:
        """
        CRT-optimized RSA decryption (demo):
        m1 = c^{dp} mod p
        m2 = c^{dq} mod q
        h = (qinv*(m1 - m2)) mod p
        m = m2 + h*q
        """
        if self.priv is None:
            raise ValueError("No private key for CRT decryption")
        if None in (self.priv.p, self.priv.q, self.priv.dp, self.priv.dq, self.priv.qinv):
            raise ValueError("CRT parameters missing in private key")

        p = self.priv.p
        q = self.priv.q
        dp = self.priv.dp
        dq = self.priv.dq
        qinv = self.priv.qinv

        m1 = modexp(c % p, dp, p)
        m2 = modexp(c % q, dq, q)
        h = (qinv * (m1 - m2)) % p
        m = m2 + h * q
        return m

    # ---- block encoding (deterministic, for demo) ----
    def _block_size(self) -> int:
        # max bytes so that block int < n
        return (self.pub.n.bit_length() - 1) // 8

    def encrypt_bytes(self, plaintext: bytes) -> List[int]:
        """
        Deterministic textbook block RSA:
        - prefix 4-byte length
        - chunk into k-byte blocks (k chosen so block < n)
        - encrypt each block
        """
        k = self._block_size()
        if k < 1:
            raise ValueError("n too small")

        data = len(plaintext).to_bytes(4, "big") + plaintext
        if len(data) % k != 0:
            data += b"\x00" * (k - (len(data) % k))

        blocks: List[int] = []
        for i in range(0, len(data), k):
            m = bytes_to_int(data[i:i + k])
            blocks.append(self.encrypt_int(m))
        return blocks

    def decrypt_bytes(self, ciphertext_blocks: List[int], use_crt: bool = False) -> bytes:
        if self.priv is None:
            raise ValueError("No private key for decryption")

        k = self._block_size()
        out = bytearray()

        for c in ciphertext_blocks:
            m = self.decrypt_int_crt(c) if use_crt else self.decrypt_int(c)
            out.extend(int_to_bytes(m, k))

        total_len = int.from_bytes(out[:4], "big")
        return bytes(out[4:4 + total_len])

    def encrypt_text(self, text: str, encoding: str = "utf-8") -> List[int]:
        return self.encrypt_bytes(text.encode(encoding))

    def decrypt_text(self, ciphertext_blocks: List[int], encoding: str = "utf-8", use_crt: bool = False) -> str:
        return self.decrypt_bytes(ciphertext_blocks, use_crt=use_crt).decode(encoding)

    # ---- textbook signature ----
    def sign(self, message: bytes) -> int:
        if self.priv is None:
            raise ValueError("No private key for signing")
        h = bytes_to_int(hashlib.sha256(message).digest()) % self.priv.n
        return modexp(h, self.priv.d, self.priv.n)

    def verify(self, message: bytes, signature: int) -> bool:
        h = bytes_to_int(hashlib.sha256(message).digest()) % self.pub.n
        h2 = modexp(signature, self.pub.e, self.pub.n)
        return h == h2
