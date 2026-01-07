import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Algorithms.utilities import is_probable_prime, generate_prime
import time


def main():
    print("=== DEMO 02: Miller–Rabin primality test + prime generation ===\n")
    print("Miller-Rabin (CLRS 31.8): probabilistic primality test")
    print("Error probability ≤ 2^(-k) where k = number of rounds\n")

    print("=" * 70)
    print("Testing known primes and composites:")
    print("=" * 70)

    tests = [
        (2, "prime"),
        (3, "prime"),
        (5, "prime"),
        (7, "prime"),
        (11, "prime"),
        (13, "prime"),
        (17, "prime"),
        (21, "composite: 3 × 7"),
        (25, "composite: 5²"),
        (27, "composite: 3³"),
        (91, "composite: 7 × 13"),
        (221, "composite: 13 × 17"),
        (341, "composite (pseudoprime to base 2)"),
        (561, "Carmichael number (pseudoprime to all bases)"),
        (1105, "Carmichael number"),
        (1729, "Carmichael number (Ramanujan's taxicab)"),
        (2465, "Carmichael number"),
        (2821, "Carmichael number"),
        (6601, "Carmichael number"),
    ]

    rounds = 20
    for n, description in tests:
        result = is_probable_prime(n, rounds=rounds)
        status = "✓ PRIME" if result else "✗ COMPOSITE"
        print(f"{n:6d} -> {status:12s}  ({description})")

    # Test with larger known primes
    print("\n" + "=" * 70)
    print("Testing larger known primes:")
    print("=" * 70)
    
    # Mersenne primes: 2^p - 1
    mersenne_primes = [
        (2**31 - 1, "Mersenne prime M31"),
        (2**61 - 1, "Mersenne prime M61"),
    ]
    
    for n, description in mersenne_primes:
        t0 = time.perf_counter()
        result = is_probable_prime(n, rounds=40)
        t1 = time.perf_counter()
        print(f"{description}")
        print(f"  Value: {n}")
        print(f"  Bit length: {n.bit_length()} bits")
        print(f"  Miller-Rabin result: {result}")
        print(f"  Time: {(t1-t0)*1000:.2f} ms\n")

    # Generate new primes
    print("=" * 70)
    print("Generating new random primes:")
    print("=" * 70)
    
    bit_sizes = [128, 256, 512]
    
    for bits in bit_sizes:
        print(f"\nGenerating {bits}-bit prime (with {rounds} M-R rounds)...")
        t0 = time.perf_counter()
        p = generate_prime(bits, rounds=rounds)
        t1 = time.perf_counter()
        
        print(f"  Generated prime bit_length: {p.bit_length()}")
        print(f"  First 50 digits: {str(p)[:50]}...")
        print(f"  Last 20 digits:  ...{str(p)[-20:]}")
        print(f"  Generation time: {(t1-t0)*1000:.2f} ms")
        
        # Verify it's really prime
        verify = is_probable_prime(p, rounds=40)
        print(f"  Verification (40 rounds): {verify}")

    print("\n" + "=" * 70)
    print("Notes:")
    print("  - Miller-Rabin is probabilistic (not deterministic)")
    print("  - Error probability ≤ 2^(-k) for k rounds")
    print("  - 40 rounds gives error probability ≤ 2^(-40) ≈ 10^(-12)")
    print("  - For RSA, this is sufficiently secure")
    print("=" * 70)


if __name__ == "__main__":
    main()