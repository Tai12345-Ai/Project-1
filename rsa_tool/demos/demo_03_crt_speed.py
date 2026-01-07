"""
Demo 03: CRT Speed Optimization
CLRS 31.5 - Chinese Remainder Theorem
"""
from .demo_utils import *

def demo_crt_speed():
    """Demo 03: Chinese Remainder Theorem optimization"""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "DEMO 03: CRT OPTIMIZATION FOR RSA DECRYPTION" + " " * 19 + "║")
    print("║" + " " * 19 + "CLRS 31.5 - Chinese Remainder Theorem" + " " * 21 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    # PHẦN 1: Algorithm Explanation
    print("=" * 80)
    print("CHINESE REMAINDER THEOREM (CRT)")
    print("=" * 80)
    print("""
Ý tưởng: Thay vì tính m = c^d mod n, ta tính:
    
Standard RSA Decryption:
    m = c^d mod n
    
CRT-based RSA Decryption:
    1. Precompute:
       dp = d mod (p-1)
       dq = d mod (q-1)
       qinv = q^(-1) mod p
    
    2. Compute:
       m1 = c^dp mod p
       m2 = c^dq mod q
    
    3. Combine using CRT:
       h = qinv × (m1 - m2) mod p
       m = m2 + h × q

Lợi ích: Tính toán modulo p và q (nhỏ hơn) thay vì modulo n (lớn)
Speedup: Khoảng 4x nhanh hơn
""")
    
    # PHẦN 2: Performance Test
    print("=" * 80)
    print("PHẦN 1: SO SÁNH HIỆU NĂNG")
    print("=" * 80)
    
    key_sizes = [512, 1024, 2048]
    iterations = 5
    
    print(f"\nChạy {iterations} lần decrypt cho mỗi key size\n")
    print(f"{'Key Size':<12} {'Normal (ms)':<15} {'CRT (ms)':<15} {'Speedup':<12} {'Improvement'}")
    print("-" * 80)
    
    for bits in key_sizes:
        # Generate key
        pub, priv = keygen(bits=bits)
        rsa = RSA(pub=pub, priv=priv)
        pub_only = RSA(pub=pub, priv=None)
        
        # Create test message
        message = ("CRT optimization test. " * 5).encode('utf-8')
        ciphertext = pub_only.encrypt_bytes(message)
        
        # Normal decryption
        times_normal = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            rsa.decrypt_bytes(ciphertext, use_crt=False)
            t1 = time.perf_counter()
            times_normal.append((t1 - t0) * 1000)
        
        avg_normal = sum(times_normal) / len(times_normal)
        
        # CRT decryption
        times_crt = []
        for _ in range(iterations):
            t0 = time.perf_counter()
            rsa.decrypt_bytes(ciphertext, use_crt=True)
            t1 = time.perf_counter()
            times_crt.append((t1 - t0) * 1000)
        
        avg_crt = sum(times_crt) / len(times_crt)
        
        speedup = avg_normal / avg_crt if avg_crt > 0 else 0
        improvement = ((avg_normal - avg_crt) / avg_normal * 100) if avg_normal > 0 else 0
        
        print(f"{bits:<12} {avg_normal:<15.2f} {avg_crt:<15.2f} {speedup:<12.2f}x {improvement:.1f}%")
    
    # PHẦN 3: Detailed Analysis
    print("\n" + "=" * 80)
    print("PHẦN 2: PHÂN TÍCH CHI TIẾT (1024-bit key)")
    print("=" * 80)
    
    bits = 1024
    pub, priv = keygen(bits=bits)
    rsa = RSA(pub=pub, priv=priv)
    
    print(f"\nKey parameters:")
    print(f"   n = {pub.n.bit_length()} bits")
    print(f"   p = {priv.p.bit_length()} bits")
    print(f"   q = {priv.q.bit_length()} bits")
    print(f"   d = {str(priv.d)[:50]}...")
    
    print(f"\nCRT precomputed values:")
    print(f"   dp = d mod (p-1) = {str(priv.dp)[:50]}...")
    print(f"   dq = d mod (q-1) = {str(priv.dq)[:50]}...")
    print(f"   qinv = q^(-1) mod p = {str(priv.qinv)[:50]}...")
    
    # Verify precomputed values
    dp_check = priv.d % (priv.p - 1)
    dq_check = priv.d % (priv.q - 1)
    qinv_check = modinv(priv.q, priv.p)
    
    print(f"\nVerification:")
    print(f"   ✓ dp correct: {dp_check == priv.dp}")
    print(f"   ✓ dq correct: {dq_check == priv.dq}")
    print(f"   ✓ qinv correct: {qinv_check == priv.qinv}")
    
    # PHẦN 4: Step-by-step CRT
    print("\n" + "=" * 80)
    print("PHẦN 3: CRT DECRYPTION STEP-BY-STEP")
    print("=" * 80)
    
    test_msg = "CRT Demo"
    print(f"\nOriginal message: \"{test_msg}\"")
    
    pub_only = RSA(pub=pub, priv=None)
    c = pub_only.encrypt_text(test_msg)
    print(f"Ciphertext block: {c[0]}")
    
    # Manual CRT calculation
    c_int = c[0]
    
    print(f"\n🔄 CRT Decryption Process:")
    print(f"\nStep 1: Compute m1 = c^dp mod p")
    m1 = pow(c_int, priv.dp, priv.p)
    print(f"   m1 = {c_int}^{priv.dp} mod {priv.p}")
    print(f"   m1 = {m1}")
    
    print(f"\nStep 2: Compute m2 = c^dq mod q")
    m2 = pow(c_int, priv.dq, priv.q)
    print(f"   m2 = {c_int}^{priv.dq} mod {priv.q}")
    print(f"   m2 = {m2}")
    
    print(f"\nStep 3: Combine using CRT")
    print(f"   h = qinv × (m1 - m2) mod p")
    h = (priv.qinv * (m1 - m2)) % priv.p
    print(f"   h = {priv.qinv} × ({m1} - {m2}) mod {priv.p}")
    print(f"   h = {h}")
    
    print(f"\n   m = m2 + h × q")
    m = m2 + h * priv.q
    print(f"   m = {m2} + {h} × {priv.q}")
    print(f"   m = {m}")
    
    # Verify
    decrypted = rsa.decrypt_text(c)
    print(f"\nDecrypted message: \"{decrypted}\"")
    print(f"✓ Match: {decrypted == test_msg}")
    
    # PHẦN 5: Why It Works
    print("\n" + "=" * 80)
    print("PHẦN 4: TẠI SAO CRT HOẠT ĐỘNG?")
    print("=" * 80)
    print("""
Toán học đằng sau:

1. RSA decryption: m ≡ c^d (mod n)
   
2. Vì n = p × q (p, q nguyên tố):
   m ≡ c^d (mod n) 
   ⟺ m ≡ c^d (mod p) AND m ≡ c^d (mod q)

3. Fermat's Little Theorem:
   a^(p-1) ≡ 1 (mod p) với gcd(a,p) = 1
   
4. Do đó:
   c^d ≡ c^(d mod (p-1)) (mod p)
   c^d ≡ c^(d mod (q-1)) (mod q)

5. CRT cho phép tính m từ (m mod p) và (m mod q)

6. Speedup: 
   - Normal: O(log³ n) với n ≈ 2048 bits
   - CRT: 2 × O(log³ (n/2)) ≈ O(log³ n) / 4
   - Thực tế: ~4x nhanh hơn
""")
    
    print("✅ Demo 03 completed!")
