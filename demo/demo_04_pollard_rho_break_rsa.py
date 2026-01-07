import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
from Algorithms.rsa import PublicKey, PrivateKey, RSA
from Algorithms.utilities import modinv
from Algorithms.pollard_rho import factor_semiprime


def trial_division_demo(n, limit=10000):
    """Simple trial division for comparison."""
    if n % 2 == 0:
        return 2
    for f in range(3, min(int(n**0.5) + 1, limit), 2):
        if n % f == 0:
            return f
    return None


def main():
    print("=== DEMO 04: Break weak RSA by factoring n with Pollard Rho ===\n")
    print("Pollard's Rho algorithm (CLRS 31.9):")
    print("  - Heuristic factoring algorithm")
    print("  - Expected time: O(n^(1/4)) for factor p")
    print("  - Much faster than trial division for large n")
    print("  - This demonstrates why RSA needs large primes!\n")
    
    # Tạo RSA yếu: n nhỏ để factor được nhanh (chỉ demo!)
    bits = 96  # Very weak! Real RSA uses 2048+ bits

    print("=" * 70)
    print(f"Generating WEAK RSA key ({bits} bits) for demonstration:")
    print("=" * 70)
    
    from Algorithms.utilities import generate_prime, gcd
    e = 65537

    p = generate_prime(bits // 2, rounds=20)
    q = generate_prime(bits // 2, rounds=20)
    while q == p:
        q = generate_prime(bits // 2, rounds=20)

    n = p * q
    phi = (p - 1) * (q - 1)
    if gcd(e, phi) != 1:
        e = 3
        while gcd(e, phi) != 1:
            e += 2
    d = modinv(e, phi)

    print(f"  p = {p} ({p.bit_length()} bits)")
    print(f"  q = {q} ({q.bit_length()} bits)")
    print(f"  n = {n} ({n.bit_length()} bits)")
    print(f"  e = {e}")
    print(f"  d = {d}\n")

    pub = PublicKey(e=e, n=n)
    priv = PrivateKey(d=d, n=n)

    victim = RSA(pub=pub, priv=priv)
    attacker_pub_only = RSA(pub=pub, priv=None)

    # Victim encrypts a secret
    secret = b"Attack me if you can!"
    ciphertext = attacker_pub_only.encrypt_bytes(secret)

    print("=" * 70)
    print("Victim's encrypted message:")
    print("=" * 70)
    print(f"Public key (e, n) is known to attacker")
    print(f"  e = {e}")
    print(f"  n = {n}")
    print(f"Ciphertext blocks: {ciphertext}\n")

    print("=" * 70)
    print("Attacker attempts to factor n:")
    print("=" * 70)
    
    # Compare trial division vs Pollard Rho
    print("\n1. Trial Division (naive approach):")
    t0 = time.perf_counter()
    trial_factor = trial_division_demo(n)
    t1 = time.perf_counter()
    
    if trial_factor:
        print(f"   Found factor: {trial_factor}")
        print(f"   Time: {(t1-t0)*1000:.4f} ms")
    else:
        print(f"   Failed to find factor in reasonable time")
        print(f"   Time: {(t1-t0)*1000:.4f} ms")
    
    print("\n2. Pollard's Rho (advanced method):")
    
    # Try multiple times in case of failure
    max_attempts = 5
    pq = None
    
    for attempt in range(1, max_attempts + 1):
        print(f"   Attempt {attempt}...")
        t0 = time.perf_counter()
        pq = factor_semiprime(n)
        t1 = time.perf_counter()
        
        if pq is not None:
            print(f"   ✓ Success! Factored in {(t1-t0)*1000:.4f} ms")
            break
        else:
            print(f"   ✗ Failed (this is probabilistic, trying again...)")
    
    if pq is None:
        print(f"\n   Pollard Rho failed after {max_attempts} attempts.")
        print("   This is rare but possible. Please run again.")
        return

    fp, fq = pq
    print(f"\n   Recovered p = {fp}")
    print(f"   Recovered q = {fq}")
    print(f"   Verification: p * q = n? {fp * fq == n}")

    # Attacker reconstructs private key
    print("\n" + "=" * 70)
    print("Reconstructing private key from factors:")
    print("=" * 70)
    
    phi2 = (fp - 1) * (fq - 1)
    d2 = modinv(e, phi2)
    
    print(f"  φ(n) = (p-1)(q-1) = {phi2}")
    print(f"  d = e^(-1) mod φ(n) = {d2}")
    print(f"  Match original d? {d2 == d}")
    
    attacker_priv = PrivateKey(d=d2, n=n)
    attacker = RSA(pub=pub, priv=attacker_priv)

    # Decrypt the secret
    print("\n" + "=" * 70)
    print("Decrypting victim's message:")
    print("=" * 70)
    
    recovered = attacker.decrypt_bytes(ciphertext)
    print(f"  Recovered plaintext: {recovered}")
    print(f"  Attack successful? {recovered == secret}")

    print("\n" + "=" * 70)
    print("Security Lessons:")
    print("=" * 70)
    print(f"  - {bits}-bit RSA is TRIVIALLY BROKEN")
    print("  - Real RSA uses 2048+ bits (1024 bits minimum)")
    print("  - With 2048 bits, Pollard Rho would take ~10^20 years")
    print("  - RSA security depends on difficulty of factoring large n")
    print("=" * 70)


if __name__ == "__main__":
    main()