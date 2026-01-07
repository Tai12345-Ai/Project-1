"""
Demo 01: Basic RSA
RSA cơ bản với step-by-step explanation
CLRS 31.7 - RSA Algorithm
"""
from .demo_utils import *

def demo_basic_rsa():
    """Demo 01: RSA cơ bản với step-by-step explanation"""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "DEMO 01: BASIC RSA CRYPTOSYSTEM" + " " * 27 + "║")
    print("║" + " " * 25 + "CLRS 31.7 - RSA Algorithm" + " " * 29 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    # BƯỚC 1: Key Generation
    print("=" * 80)
    print("BƯỚC 1: KEY GENERATION")
    print("=" * 80)
    
    bits = 512
    print(f"Sinh cặp khóa RSA {bits}-bit...\n")
    
    pub, priv = keygen(bits=bits)
    
    print(f"📊 Thông số khóa:")
    print(f"   • Public exponent:  e = {pub.e}")
    print(f"   • Modulus:          n = {pub.n}")
    print(f"   • n bit length:         {pub.n.bit_length()} bits")
    print(f"\n   • Prime p:          p = {priv.p}")
    print(f"   • Prime q:          q = {priv.q}")
    print(f"   • Private exponent: d = {priv.d}")
    
    # Verify n = p × q
    print(f"\n✓ Verification: n = p × q")
    print(f"  {pub.n} = {priv.p} × {priv.q}")
    print(f"  Correct: {pub.n == priv.p * priv.q}")
    
    # Verify φ(n)
    phi = (priv.p - 1) * (priv.q - 1)
    print(f"\n✓ Euler's totient: φ(n) = (p-1)(q-1)")
    print(f"  φ(n) = {phi}")
    
    # Verify e × d ≡ 1 (mod φ(n))
    print(f"\n✓ Private key verification: e × d ≡ 1 (mod φ(n))")
    print(f"  e × d mod φ(n) = {(pub.e * priv.d) % phi}")
    print(f"  Correct: {(pub.e * priv.d) % phi == 1}")
    
    # BƯỚC 2: Encryption
    print("\n" + "=" * 80)
    print("BƯỚC 2: ENCRYPTION - Mã hóa tin nhắn")
    print("=" * 80)
    
    alice = RSA(pub=pub, priv=priv)
    pub_only = RSA(pub=pub, priv=None)
    
    messages = [
        "Hello RSA!",
        "CLRS Chapter 31",
        "Cryptography"
    ]
    
    for i, msg in enumerate(messages, 1):
        print(f"\n📝 Message {i}: \"{msg}\"")
        
        # Encrypt
        t0 = time.perf_counter()
        ciphertext = pub_only.encrypt_text(msg)
        t1 = time.perf_counter()
        
        print(f"   Encrypted to {len(ciphertext)} block(s)")
        print(f"   Time: {(t1-t0)*1000:.2f} ms")
        
        if len(ciphertext) <= 2:
            for j, c in enumerate(ciphertext):
                print(f"   Block {j+1}: {c}")
        else:
            print(f"   Block 1: {ciphertext[0]}")
            print(f"   ... ({len(ciphertext)-2} more blocks)")
            print(f"   Block {len(ciphertext)}: {ciphertext[-1]}")
        
        # Decrypt
        t0 = time.perf_counter()
        plaintext = alice.decrypt_text(ciphertext)
        t1 = time.perf_counter()
        
        print(f"   Decrypted: \"{plaintext}\"")
        print(f"   Time: {(t1-t0)*1000:.2f} ms")
        print(f"   ✓ Match: {plaintext == msg}")
    
    # BƯỚC 3: Digital Signature
    print("\n" + "=" * 80)
    print("BƯỚC 3: DIGITAL SIGNATURE - Chữ ký số")
    print("=" * 80)
    
    documents = [
        "I owe Bob $100",
        "Contract signed on 2026-01-07",
        "Transfer approved"
    ]
    
    for i, doc in enumerate(documents, 1):
        print(f"\n📄 Document {i}: \"{doc}\"")
        
        # Sign
        doc_bytes = doc.encode('utf-8')
        t0 = time.perf_counter()
        signature = alice.sign(doc_bytes)
        t1 = time.perf_counter()
        
        sig_str = str(signature)
        print(f"   Signature: {sig_str[:50]}...{sig_str[-20:]}")
        print(f"   Sign time: {(t1-t0)*1000:.2f} ms")
        
        # Verify
        t0 = time.perf_counter()
        valid = pub_only.verify(doc_bytes, signature)
        t1 = time.perf_counter()
        
        print(f"   ✓ Signature valid: {valid}")
        print(f"   Verify time: {(t1-t0)*1000:.2f} ms")
        
        # Tamper test
        tampered = (doc + " MODIFIED").encode('utf-8')
        valid_tampered = pub_only.verify(tampered, signature)
        print(f"   ✗ Tampered document valid: {valid_tampered}")
    
    # BƯỚC 4: Deterministic Test
    print("\n" + "=" * 80)
    print("BƯỚC 4: DETERMINISTIC PROPERTY TEST")
    print("=" * 80)
    
    test_msg = "Same message"
    print(f"\n🔄 Encrypting \"{test_msg}\" multiple times:")
    
    ciphertexts = []
    for i in range(3):
        c = pub_only.encrypt_text(test_msg)
        ciphertexts.append(c)
        print(f"   Attempt {i+1}: {c[0] if c else 'N/A'}")
    
    all_same = all(c == ciphertexts[0] for c in ciphertexts)
    print(f"\n⚠️  All ciphertexts identical: {all_same}")
    if all_same:
        print("   This is a security vulnerability in textbook RSA!")
    
    print("\n✅ Demo 01 completed!")
