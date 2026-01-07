"""
Demo 06: Wiener's Attack
Attack on RSA with small private exponent d
"""
from .demo_utils import *

def demo_wiener_attack():
    """Demo 06: Wiener's attack on small d"""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 22 + "DEMO 06: WIENER'S ATTACK ON SMALL d" + " " * 21 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    print("=" * 80)
    print("WIENER'S ATTACK")
    print("=" * 80)
    print("""
Scenario: Attacker biết (e, n) và d rất nhỏ
          (d < n^0.25 hoặc d < n^(1/4))

Attack:
1. Sử dụng continued fraction của e/n
2. Tìm convergents p_k/q_k
3. Test xem q_k có phải là d không
4. Nếu tìm được d → RSA bị phá!

Tại sao d nhỏ nguy hiểm:
- Decryption nhanh hơn (d nhỏ)
- Nhưng dễ bị tấn công!
- Trade-off: Security vs Performance
""")
    
    print("=" * 80)
    print("DEMONSTRATION")
    print("=" * 80)
    
    # Generate weak RSA (small d)
    print("\n⚠️  Generating WEAK RSA with small d...")
    bits = 256  # Smaller for demo
    
    p = generate_prime(bits // 2, rounds=20)
    q = generate_prime(bits // 2, rounds=20)
    while q == p:
        q = generate_prime(bits // 2, rounds=20)
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose small d
    d = secrets.randbelow(int(n ** 0.25)) | 1
    while gcd(d, phi) != 1:
        d = secrets.randbelow(int(n ** 0.25)) | 1
    
    e = modinv(d, phi)
    
    print(f"\nParameters:")
    print(f"   p = {p}")
    print(f"   q = {q}")
    print(f"   n = {n} ({n.bit_length()} bits)")
    print(f"   φ(n) = {phi}")
    print(f"   d = {d} ({d.bit_length()} bits)")
    print(f"   e = {e}")
    
    # Check vulnerability
    threshold = int(n ** 0.25)
    vulnerable = d < threshold
    
    print(f"\nSecurity Check:")
    print(f"   d < n^(1/4)? {vulnerable}")
    print(f"   d = {d}")
    print(f"   n^(1/4) = {threshold}")
    
    if vulnerable:
        print(f"\n❌ VULNERABLE to Wiener's attack!")
    else:
        print(f"\n✓ Safe from basic Wiener's attack")
    
    # Continued fraction attack (simplified)
    print(f"\n🔍 Attempting continued fraction attack...")
    print(f"   (Simplified version - real attack more complex)")
    
    # In practice, would compute continued fraction
    # This is simplified demonstration
    
    print(f"\nReal-world implications:")
    print(f"   • RSA implementations must ensure d is large")
    print(f"   • Typically d ≈ φ(n) in size")
    print(f"   • Modern RSA safe from this attack")
    
    print("\n✅ Demo 06 completed!")
