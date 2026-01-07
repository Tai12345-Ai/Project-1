"""
Demo 05: Textbook RSA Vulnerabilities
Security analysis of unpadded RSA
"""
from .demo_utils import *

def demo_textbook_padding():
    """Demo 05: Textbook RSA vulnerabilities"""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "DEMO 05: TEXTBOOK RSA SECURITY VULNERABILITIES" + " " * 17 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    pub, priv = keygen(bits=512)
    rsa = RSA(pub=pub, priv=priv)
    pub_only = RSA(pub=pub, priv=None)
    
    # VULNERABILITY 1: Deterministic
    print("=" * 80)
    print("VULNERABILITY 1: DETERMINISTIC ENCRYPTION")
    print("=" * 80)
    
    msg = b"secret password"
    print(f"\nMessage: {msg}")
    print("\nMã hóa 5 lần:")
    
    ciphertexts = []
    for i in range(5):
        c = pub_only.encrypt_bytes(msg)
        ciphertexts.append(c)
        print(f"  #{i+1}: {c[0]}")
    
    all_same = all(c == ciphertexts[0] for c in ciphertexts)
    print(f"\n❌ Tất cả giống nhau: {all_same}")
    print("   → Attacker có thể nhận ra message giống nhau")
    print("   → Dictionary attack có thể thành công")
    
    # VULNERABILITY 2: Homomorphic Property
    print("\n" + "=" * 80)
    print("VULNERABILITY 2: HOMOMORPHIC PROPERTY")
    print("=" * 80)
    
    print("\nTính chất: E(m₁) × E(m₂) = E(m₁ × m₂)")
    
    m1 = 42
    m2 = 100
    
    # Encrypt individually
    c1 = pow(m1, pub.e, pub.n)
    c2 = pow(m2, pub.e, pub.n)
    
    # Multiply ciphertexts
    c_mult = (c1 * c2) % pub.n
    
    # Decrypt
    d_mult = pow(c_mult, priv.d, pub.n)
    
    print(f"\nm₁ = {m1}")
    print(f"m₂ = {m2}")
    print(f"c₁ = E(m₁) = {c1}")
    print(f"c₂ = E(m₂) = {c2}")
    print(f"c₁ × c₂ mod n = {c_mult}")
    print(f"D(c₁ × c₂) = {d_mult}")
    print(f"m₁ × m₂ = {m1 * m2}")
    print(f"\n✓ Verified: {d_mult == (m1 * m2) % pub.n}")
    
    print("\n❌ Attacker có thể modify ciphertext:")
    print("   - Nhân với 2^e để double plaintext")
    print("   - Blind signature attack")
    
    # VULNERABILITY 3: Malleability
    print("\n" + "=" * 80)
    print("VULNERABILITY 3: MALLEABILITY ATTACK")
    print("=" * 80)
    
    amount = 100
    print(f"\nAlice encrypts: ${amount}")
    
    c_orig = pow(amount, pub.e, pub.n)
    print(f"Ciphertext: {c_orig}")
    
    # Eve intercepts and modifies
    multiplier = 10
    factor_e = pow(multiplier, pub.e, pub.n)
    c_modified = (c_orig * factor_e) % pub.n
    
    print(f"\n🕵️  Eve modifies ciphertext:")
    print(f"  c' = c × {multiplier}^e mod n")
    print(f"  c' = {c_modified}")
    
    # Bob decrypts
    m_decrypted = pow(c_modified, priv.d, pub.n)
    print(f"\nBob decrypts: ${m_decrypted}")
    print(f"❌ Amount changed from ${amount} to ${m_decrypted}!")
    
    # SOLUTION: Padding
    print("\n" + "=" * 80)
    print("SOLUTION: PADDING SCHEMES")
    print("=" * 80)
    print("""
PKCS#1 v1.5 Padding:
    EM = 0x00 || 0x02 || PS || 0x00 || M
    PS = random padding string

RSA-OAEP (Optimal Asymmetric Encryption Padding):
    EM = 0x00 || maskedSeed || maskedDB
    Uses hash functions and randomness
    
Benefits:
    ✓ Non-deterministic (random padding)
    ✓ Prevents known-plaintext attacks
    ✓ Semantic security
    ✓ Prevents malleability

⚠️  NEVER use textbook RSA in production!
    Always use proper padding (OAEP recommended)
""")
    
    print("✅ Demo 05 completed!")
