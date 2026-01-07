from __future__ import annotations
import secrets
from typing import Optional, Tuple

from .utilities import gcd, modexp, is_probable_prime


def _trial_division(n: int, limit: int = 10000) -> Optional[int]:
    """Quickly remove small factors."""
    if n % 2 == 0:
        return 2
    f = 3
    while f * f <= n and f <= limit:
        if n % f == 0:
            return f
        f += 2
    return None


def pollard_rho(n: int) -> Optional[int]:
    """
    Pollard's Rho to find a non-trivial factor of n (heuristic).
    Returns a factor or None if failed.
    """
    if n % 2 == 0:
        return 2
    if n <= 1:
        return None
    if is_probable_prime(n, rounds=12):
        return None  # n is prime

    small = _trial_division(n)
    if small is not None and small != n:
        return small

    # Try multiple random polynomials/starts
    for _ in range(25):
        c = secrets.randbelow(n - 1) + 1
        x = secrets.randbelow(n - 2) + 2
        y = x
        d = 1

        # f(x) = x^2 + c mod n
        def f(v: int) -> int:
            return (v * v + c) % n

        # Floyd cycle detection
        for _ in range(20000):
            x = f(x)
            y = f(f(y))
            d = gcd(abs(x - y), n)
            if d == 1:
                continue
            if d == n:
                break
            return d

    return None


def factor_semiprime(n: int) -> Optional[Tuple[int, int]]:
    """
    Try factor n into (p,q) assuming n is a semiprime for demo.
    """
    if n <= 1:
        return None

    f = pollard_rho(n)
    if f is None:
        return None
    p = f
    q = n // f
    if p * q != n:
        return None
    if p > q:
        p, q = q, p
    return (p, q)
