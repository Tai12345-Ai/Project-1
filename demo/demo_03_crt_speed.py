import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
from Algorithms.rsa import keygen, RSA


def main():
    print("=== DEMO 03: CRT speedup for RSA decryption ===\n")
    print("Chinese Remainder Theorem (CLRS 31.5) optimization:")
    print("  Normal: m = c^d mod n")
    print("  CRT:    m1 = c^dp mod p,  m2 = c^dq mod q")
    print("          then combine using CRT")
    print("  Speedup: ~4x faster (exponents are half size)\n")
    
    pub, priv = keygen(bits=1024)  # CRT demo nên để 1024 cho thấy khác biệt rõ
    rsa = RSA(pub=pub, priv=priv)
    pub_only = RSA(pub=pub, priv=None)

    print("=" * 70)
    print("RSA Parameters:")
    print("=" * 70)
    print(f"n bit length: {pub.n.bit_length()} bits")
    print(f"p bit length: {priv.p.bit_length()} bits")
    print(f"q bit length: {priv.q.bit_length()} bits")
    print(f"d bit length: {priv.d.bit_length()} bits")
    print(f"dp bit length: {priv.dp.bit_length()} bits  (dp = d mod (p-1))")
    print(f"dq bit length: {priv.dq.bit_length()} bits  (dq = d mod (q-1))")
    print(f"qinv: {priv.qinv}  (q^(-1) mod p)\n")

    message = ("CRT makes RSA private operations faster. " * 20).encode("utf-8")
    print(f"Message length: {len(message)} bytes")
    
    ciphertext_blocks = pub_only.encrypt_bytes(message)
    print(f"Number of ciphertext blocks: {len(ciphertext_blocks)}\n")

    # Warm up (first runs may be slower due to Python JIT/caching)
    print("Warming up...")
    rsa.decrypt_bytes(ciphertext_blocks, use_crt=False)
    rsa.decrypt_bytes(ciphertext_blocks, use_crt=True)

    iterations = 30
    print(f"Running {iterations} iterations for each method...\n")

    # Time normal decrypt
    print("Testing normal decryption (c^d mod n)...")
    t0 = time.perf_counter()
    for _ in range(iterations):
        pt = rsa.decrypt_bytes(ciphertext_blocks, use_crt=False)
    t1 = time.perf_counter()

    # Time CRT decrypt
    print("Testing CRT decryption...")
    t2 = time.perf_counter()
    for _ in range(iterations):
        pt2 = rsa.decrypt_bytes(ciphertext_blocks, use_crt=True)
    t3 = time.perf_counter()

    # Verify correctness
    assert pt == message, "Normal decryption failed!"
    assert pt2 == message, "CRT decryption failed!"
    print("Both methods produce correct results ✓\n")

    normal = t1 - t0
    crt = t3 - t2

    print("=" * 70)
    print("Performance Results:")
    print("=" * 70)
    print(f"Normal decrypt total: {normal:.4f}s  ({normal/iterations*1000:.2f} ms/iter)")
    print(f"CRT decrypt total:    {crt:.4f}s  ({crt/iterations*1000:.2f} ms/iter)")
    if crt > 0:
        speedup = normal / crt
        print(f"\nSpeedup: {speedup:.2f}x faster with CRT")
        print(f"Time saved: {(1 - 1/speedup)*100:.1f}%")
    
    print("\n" + "=" * 70)
    print("Why CRT is faster:")
    print("  - Exponents (dp, dq) are ~half the size of d")
    print("  - Modular exponentiation cost is O(log³ exponent)")
    print("  - Working mod p and mod q (half size) vs mod n")
    print("  - Theoretical speedup: 4x (in practice: 2-4x)")
    print("=" * 70)


if __name__ == "__main__":
    main()