"""
Demo 08: RSA Mathematical Properties
Exploring the mathematical foundations of RSA
"""
from .demo_utils import *

def demo_rsa_properties():
    """Demo 08: Mathematical properties of RSA"""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "DEMO 08: RSA MATHEMATICAL PROPERTIES" + " " * 22 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    pub, priv = keygen(bits=512)
    n = pub.n
    e = pub.e
    d = priv.d
    p = priv.p
    q = priv.q
    phi = (p - 1) * (q - 1)
    
    # PROPERTY 1: Correctness
    print("=" * 80)
    print("PROPERTY 1: CORRECTNESS - (m^e)^d ≡ m (mod n)")
    print("=" * 80)
    
    test_messages = [42, 12345, 99999]
    
    print("\nTest với nhiều message:")
    for m in test_messages:
        c = pow(m, e, n)
        m_recovered = pow(c, d, n)
        print(f"\n  m = {m}")
        print(f"  c = m^e mod n = {c}")
        print(f"  m' = c^d mod n = {m_recovered}")
        print(f"  ✓ Correct: {m == m_recovered}")
    
    # PROPERTY 2: Euler's theorem
    print("\n" + "=" * 80)
    print("PROPERTY 2: EULER'S THEOREM - m^φ(n) ≡ 1 (mod n)")
    print("=" * 80)
    
    m = 12345
    print(f"\nm = {m}")
    print(f"φ(n) = (p-1)(q-1) = {phi}")
    
    result = pow(m, phi, n)
    print(f"\nm^φ(n) mod n = {m}^{phi} mod {n}")
    print(f"             = {result}")
    print(f"✓ Equals 1: {result == 1}")
    
    # PROPERTY 3: Key relationship
    print("\n" + "=" * 80)
    print("PROPERTY 3: KEY RELATIONSHIP - e·d ≡ 1 (mod φ(n))")
    print("=" * 80)
    
    print(f"\ne = {e}")
    print(f"d = {d}")
    print(f"φ(n) = {phi}")
    
    ed_mod_phi = (e * d) % phi
    print(f"\ne·d mod φ(n) = {e} · {d} mod {phi}")
    print(f"              = {ed_mod_phi}")
    print(f"✓ Equals 1: {ed_mod_phi == 1}")
    
    # PROPERTY 4: Commutativity
    print("\n" + "=" * 80)
    print("PROPERTY 4: COMMUTATIVITY - Encrypt then Decrypt = Decrypt then Encrypt")
    print("=" * 80)
    
    m = 42
    print(f"\nMessage: m = {m}")
    
    # Path 1: Encrypt then decrypt
    c = pow(m, e, n)
    m1 = pow(c, d, n)
    print(f"\nPath 1: Encrypt → Decrypt")
    print(f"  c = m^e mod n = {c}")
    print(f"  m = c^d mod n = {m1}")
    
    # Path 2: "Decrypt" then "encrypt" (sign then verify)
    s = pow(m, d, n)
    m2 = pow(s, e, n)
    print(f"\nPath 2: Sign (use d) → Verify (use e)")
    print(f"  s = m^d mod n = {s}")
    print(f"  m = s^e mod n = {m2}")
    
    print(f"\n✓ Both paths recover m: {m1 == m2 == m}")
    
    # PROPERTY 5: Homomorphic
    print("\n" + "=" * 80)
    print("PROPERTY 5: MULTIPLICATIVE HOMOMORPHIC")
    print("=" * 80)
    
    m1 = 10
    m2 = 20
    
    c1 = pow(m1, e, n)
    c2 = pow(m2, e, n)
    c_mult = (c1 * c2) % n
    
    m_mult = pow(c_mult, d, n)
    m_expected = (m1 * m2) % n
    
    print(f"\nm₁ = {m1}, m₂ = {m2}")
    print(f"E(m₁) = {c1}")
    print(f"E(m₂) = {c2}")
    print(f"E(m₁) · E(m₂) mod n = {c_mult}")
    print(f"D(E(m₁) · E(m₂)) = {m_mult}")
    print(f"m₁ · m₂ mod n = {m_expected}")
    print(f"✓ Equal: {m_mult == m_expected}")
    
    print("\n⚠️  Security implication: Malleability!")
    
    # PROPERTY 6: Chinese Remainder Theorem
    print("\n" + "=" * 80)
    print("PROPERTY 6: CRT - Efficient computation using p and q")
    print("=" * 80)
    
    m = 12345
    c = pow(m, e, n)
    
    # Method 1: Direct
    m_direct = pow(c, d, n)
    
    # Method 2: CRT
    dp = d % (p - 1)
    dq = d % (q - 1)
    qinv = modinv(q, p)
    
    m1 = pow(c, dp, p)
    m2 = pow(c, dq, q)
    h = (qinv * (m1 - m2)) % p
    m_crt = m2 + h * q
    
    print(f"\nMessage: m = {m}")
    print(f"Ciphertext: c = {c}")
    
    print(f"\nMethod 1 (Direct):")
    print(f"  m = c^d mod n = {m_direct}")
    
    print(f"\nMethod 2 (CRT):")
    print(f"  m₁ = c^dp mod p = {m1}")
    print(f"  m₂ = c^dq mod q = {m2}")
    print(f"  h = qinv·(m₁-m₂) mod p = {h}")
    print(f"  m = m₂ + h·q = {m_crt}")
    
    print(f"\n✓ Both methods equal: {m_direct == m_crt}")
    
    print("\n✅ Demo 08 completed!")
