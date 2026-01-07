"""
Demo 04: Pollard's Rho Factorization
CLRS 31.9 - Integer Factorization
"""
from .demo_utils import *

def demo_pollard_rho():
    """Demo 04: Pollard Rho factorization"""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 18 + "DEMO 04: POLLARD'S RHO FACTORIZATION" + " " * 24 + "║")
    print("║" + " " * 24 + "CLRS 31.9 - Integer Factorization" + " " * 23 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    print("=" * 80)
    print("POLLARD'S RHO ALGORITHM")
    print("=" * 80)
    print("""
Mục đích: Phân tích n = p × q để tìm p và q
    
Algorithm:
1. Chọn hàm f(x) = (x² + c) mod n
2. Bắt đầu với x₀ ngẫu nhiên
3. Tính dãy: x₁ = f(x₀), x₂ = f(x₁), ...
4. Dùng Floyd's cycle detection:
   - Tortoise: xᵢ
   - Hare: x₂ᵢ
5. Tính gcd(|xᵢ - x₂ᵢ|, n)
6. Nếu 1 < gcd < n: Tìm thấy factor!

Complexity: O(√p) với p là factor nhỏ nhất
""")
    
    # Test với các key sizes khác nhau
    print("=" * 80)
    print("PHẦN 1: FACTORIZATION TESTS")
    print("=" * 80)
    
    test_sizes = [40, 64, 96, 128]
    
    print(f"\n{'Bits':<8} {'n value':<35} {'Time (ms)':<12} {'Result'}")
    print("-" * 80)
    
    for bits in test_sizes:
        # Generate weak RSA
        p = generate_prime(bits // 2, rounds=20)
        q = generate_prime(bits // 2, rounds=20)
        while q == p:
            q = generate_prime(bits // 2, rounds=20)
        
        n = p * q
        n_str = str(n)[:30] + "..." if len(str(n)) > 30 else str(n)
        
        # Factor with Pollard Rho
        t0 = time.perf_counter()
        result = factor_semiprime(n)
        t1 = time.perf_counter()
        
        elapsed = (t1 - t0) * 1000
        
        if result:
            p_found, q_found = result
            status = "✓ Success" if (p_found == p or p_found == q) else "✗ Wrong"
            print(f"{bits:<8} {n_str:<35} {elapsed:<12.2f} {status}")
        else:
            print(f"{bits:<8} {n_str:<35} {elapsed:<12.2f} ✗ Failed")
    
    # Detailed example
    print("\n" + "=" * 80)
    print("PHẦN 2: CHI TIẾT PHÂN TÍCH")
    print("=" * 80)
    
    bits = 80
    print(f"\nTạo RSA yếu {bits}-bit:")
    p = generate_prime(bits // 2, rounds=20)
    q = generate_prime(bits // 2, rounds=20)
    while q == p:
        q = generate_prime(bits // 2, rounds=20)
    
    n = p * q
    
    print(f"   p = {p} ({p.bit_length()} bits)")
    print(f"   q = {q} ({q.bit_length()} bits)")
    print(f"   n = {n} ({n.bit_length()} bits)")
    
    print(f"\nChạy Pollard's Rho...")
    t0 = time.perf_counter()
    result = factor_semiprime(n)
    t1 = time.perf_counter()
    
    if result:
        p_found, q_found = result
        print(f"\n✓ Phân tích thành công!")
        print(f"   p = {p_found}")
        print(f"   q = {q_found}")
        print(f"   Verify: p × q = {p_found * q_found}")
        print(f"   Match: {p_found * q_found == n}")
        print(f"   Time: {(t1-t0)*1000:.2f} ms")
    
    print("\n" + "=" * 80)
    print("PHẦN 3: TẠI SAO RSA CẦN PRIMES LỚN")
    print("=" * 80)
    print("""
Bảo mật RSA phụ thuộc vào độ khó factorization:

┌─────────────┬──────────────────┬─────────────────────────────┐
│  Key Size   │  Time to Factor  │  Security Level             │
├─────────────┼──────────────────┼─────────────────────────────┤
│  512-bit    │  Hours/Days      │  ✗ Insecure (broken 1999)   │
│  768-bit    │  Weeks/Months    │  ✗ Insecure (broken 2009)   │
│  1024-bit   │  Years           │  ⚠️  Weak (deprecated)       │
│  2048-bit   │  Infeasible      │  ✓ Secure (recommended)     │
│  3072-bit   │  Infeasible      │  ✓ High security            │
│  4096-bit   │  Infeasible      │  ✓ Maximum security         │
└─────────────┴──────────────────┴─────────────────────────────┘

Pollard's Rho: O(√p) ≈ O(2^(bits/4))
General Number Field Sieve (GNFS): O(e^((log n)^(1/3)))

⚠️  Quantum computers (Shor's algorithm): O((log n)²)
    → RSA sẽ không an toàn với quantum computers!
""")
    
    print("✅ Demo 04 completed!")
