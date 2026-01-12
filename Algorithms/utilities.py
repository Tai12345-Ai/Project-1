from __future__ import annotations
import secrets
from typing import Tuple


def gcd(a: int, b: int) -> int:
    """Euclid GCD (CLRS 31.2)."""
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """
    Extended Euclid (CLRS 31.2) - Iterative version to avoid recursion limit.
    Returns (d, x, y) such that ax + by = d = gcd(a,b).
    """
    # Make a, b positive
    a, b = abs(a), abs(b)
    
    # Iterative version
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    
    return (old_r, old_s, old_t)


def modinv(a: int, n: int) -> int:
    """Modular inverse using extended gcd."""
    d, x, _ = extended_gcd(a, n)
    if d != 1:
        raise ValueError("No modular inverse exists because gcd(a, n) != 1")
    return x % n


def modexp(a: int, b: int, n: int) -> int:
    """Modular exponentiation by repeated squaring (CLRS 31.6)."""
    if n == 1:
        return 0
    result = 1
    a %= n
    while b > 0:
        if b & 1:
            result = (result * a) % n
        a = (a * a) % n
        b >>= 1
    return result


def is_probable_prime(n: int, rounds: int = 40) -> bool:
    """
    Miller-Rabin primality test (CLRS 31.8).
    rounds ~ number of random bases; error probability decreases exponentially.
    """
    if n in (2, 3):
        return True
    if n <= 1 or (n % 2 == 0):
        return False

    # write n-1 = 2^t * u with u odd
    u = n - 1
    t = 0
    while u % 2 == 0:
        u //= 2
        t += 1

    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2  # [2, n-2]
        x = modexp(a, u, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(t - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits: int, rounds: int = 40) -> int:
    """Generate a probable prime of given bit length using Miller-Rabin."""
    if bits < 2:
        raise ValueError("bits must be >= 2")

    while True:
        p = secrets.randbits(bits)
        p |= (1 << (bits - 1))  # ensure top bit set
        p |= 1                  # ensure odd
        if is_probable_prime(p, rounds=rounds):
            return p


def bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, "big")


def int_to_bytes(x: int, length: int) -> bytes:
    return x.to_bytes(length, "big")
