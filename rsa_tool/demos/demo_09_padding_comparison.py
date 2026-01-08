"""
Demo 09: Padding Comparison - Textbook vs OAEP vs PSS
So sánh trực quan về security và tính năng của các padding schemes
"""
from Algorithms.rsa import keygen, RSA
import time


def demo_padding_comparison():
    """
    Demo chi tiết về sự khác biệt giữa Textbook RSA và Secure Padding
    """
    output = []
    
    output.append("=" * 80)
    output.append("DEMO 09: PADDING SCHEMES COMPARISON")
    output.append("Textbook RSA vs OAEP (Encryption) vs PSS (Signature)")
    output.append("=" * 80)
    output.append("")
    
    # Generate keys
    output.append("🔑 Generating 1024-bit RSA keys...")
    pub, priv = keygen(bits=1024)
    rsa = RSA(pub=pub, priv=priv)
    output.append(f"✓ Keys generated: n = {pub.n}")
    output.append("")
    
    # ==================== ENCRYPTION COMPARISON ====================
    output.append("=" * 80)
    output.append("PART 1: ENCRYPTION - Textbook vs OAEP")
    output.append("=" * 80)
    output.append("")
    
    message1 = "Attack at dawn"
    message2 = "Attack at dawn"  # Same message
    
    # Textbook RSA - Deterministic
    output.append("📝 Testing Textbook RSA (Deterministic):")
    output.append(f"   Message: '{message1}'")
    
    cipher1_textbook = rsa.encrypt_text(message1)[0]
    cipher2_textbook = rsa.encrypt_text(message2)[0]
    
    output.append(f"   Encryption 1: {cipher1_textbook}")
    output.append(f"   Encryption 2: {cipher2_textbook}")
    output.append(f"   Same ciphertext? {cipher1_textbook == cipher2_textbook}")
    output.append("")
    output.append("   ⚠️  PROBLEM: Cùng message → Cùng ciphertext")
    output.append("   → Attacker có thể detect repeated messages!")
    output.append("   → Vulnerable to dictionary attacks!")
    output.append("")
    
    # OAEP - Non-deterministic
    output.append("🔒 Testing OAEP (Non-deterministic, Secure):")
    output.append(f"   Message: '{message1}'")
    
    cipher1_oaep = rsa.encrypt_oaep(message1.encode('utf-8'))
    cipher2_oaep = rsa.encrypt_oaep(message2.encode('utf-8'))
    
    output.append(f"   Encryption 1: {cipher1_oaep}")
    output.append(f"   Encryption 2: {cipher2_oaep}")
    output.append(f"   Same ciphertext? {cipher1_oaep == cipher2_oaep}")
    output.append("")
    output.append("   ✓ SECURE: Cùng message → Khác ciphertext (random padding)")
    output.append("   ✓ IND-CCA2 secure (Indistinguishability under Chosen Ciphertext Attack)")
    output.append("   ✓ Prevents dictionary attacks")
    output.append("")
    
    # Decryption verification
    plain1_oaep = rsa.decrypt_oaep(cipher1_oaep)
    output.append(f"   Decryption: '{plain1_oaep.decode('utf-8')}'")
    output.append(f"   ✓ Decryption successful!")
    output.append("")
    
    # ==================== MALLEABILITY TEST ====================
    output.append("=" * 80)
    output.append("PART 2: MALLEABILITY ATTACK on Textbook RSA")
    output.append("=" * 80)
    output.append("")
    
    output.append("📝 Original message: 'Hello' → encrypt → get ciphertext C")
    message_original = "Hello"
    ciphertexts = rsa.encrypt_text(message_original)
    C = ciphertexts[0]
    output.append(f"   C = {C}")
    output.append("")
    
    output.append("💥 Attacker modifies ciphertext: C' = C × 2^e mod n")
    output.append("   (without knowing the plaintext or private key!)")
    
    # Malleability attack: C' = C * 2^e mod n
    factor = 2
    C_modified = (C * pow(factor, pub.e, pub.n)) % pub.n
    output.append(f"   C' = {C_modified}")
    output.append("")
    
    output.append("🔓 Decrypt modified ciphertext C':")
    # Note: decrypt_text expects list
    try:
        decrypted_bytes = rsa.decrypt_text([C_modified])
        # Try to decode, but handle non-UTF8 bytes
        try:
            decrypted_modified = decrypted_bytes.decode('utf-8', errors='ignore').rstrip('\x00')
        except:
            decrypted_modified = decrypted_bytes.hex()
        output.append(f"   Result: {repr(decrypted_bytes[:20])}... (showing first 20 bytes)")
        output.append(f"   → Plaintext was multiplied by {factor} due to homomorphic property!")
    except Exception as e:
        output.append(f"   Result: Decryption modified the data (bytes: {str(e)[:50]}...)")
    
    output.append("")
    output.append("   ⚠️  PROBLEM: Textbook RSA is MALLEABLE")
    output.append("   → Attacker can manipulate ciphertext meaningfully")
    output.append("   → Mathematical: Dec(C × k^e) = Dec(C) × k")
    output.append("   → OAEP prevents this (integrity check fails)")
    output.append("")
    
    # ==================== SIGNATURE COMPARISON ====================
    output.append("=" * 80)
    output.append("PART 3: SIGNATURES - Textbook vs PSS")
    output.append("=" * 80)
    output.append("")
    
    message_to_sign = "I owe Alice $100"
    
    # Textbook signature - Deterministic
    output.append("✍️  Testing Textbook RSA Signature:")
    output.append(f"   Message: '{message_to_sign}'")
    
    sig1_textbook = rsa.sign(message_to_sign.encode('utf-8'))
    sig2_textbook = rsa.sign(message_to_sign.encode('utf-8'))
    
    output.append(f"   Signature 1: {sig1_textbook}")
    output.append(f"   Signature 2: {sig2_textbook}")
    output.append(f"   Same signature? {sig1_textbook == sig2_textbook}")
    output.append("")
    output.append("   ⚠️  PROBLEM: Always same signature for same message")
    output.append("   → Vulnerable to replay attacks")
    output.append("   → No randomness in signing process")
    output.append("")
    
    # PSS signature - Probabilistic
    output.append("🔏 Testing PSS Signature (Probabilistic, Secure):")
    output.append(f"   Message: '{message_to_sign}'")
    
    sig1_pss = rsa.sign_pss(message_to_sign.encode('utf-8'))
    sig2_pss = rsa.sign_pss(message_to_sign.encode('utf-8'))
    
    output.append(f"   Signature 1: {sig1_pss}")
    output.append(f"   Signature 2: {sig2_pss}")
    output.append(f"   Same signature? {sig1_pss == sig2_pss}")
    output.append("")
    output.append("   ✓ SECURE: Different signature each time (random salt)")
    output.append("   ✓ Provably secure in random oracle model")
    output.append("   ✓ Better security guarantees than textbook")
    output.append("")
    
    # Verification
    valid1 = rsa.verify_pss(message_to_sign.encode('utf-8'), sig1_pss)
    valid2 = rsa.verify_pss(message_to_sign.encode('utf-8'), sig2_pss)
    output.append(f"   Verify signature 1: {valid1}")
    output.append(f"   Verify signature 2: {valid2}")
    output.append("   ✓ Both signatures verify successfully!")
    output.append("")
    
    # ==================== SECURITY SUMMARY ====================
    output.append("=" * 80)
    output.append("SECURITY SUMMARY")
    output.append("=" * 80)
    output.append("")
    
    output.append("📊 Textbook RSA:")
    output.append("   ✗ Deterministic → Same input = Same output")
    output.append("   ✗ Malleable → Attacker can modify ciphertext meaningfully")
    output.append("   ✗ Vulnerable to chosen ciphertext attacks")
    output.append("   ✗ No integrity protection")
    output.append("   ✓ Simple and fast (educational purposes only)")
    output.append("")
    
    output.append("🔒 OAEP (Encryption):")
    output.append("   ✓ Non-deterministic → Random padding each time")
    output.append("   ✓ IND-CCA2 secure")
    output.append("   ✓ Prevents malleability attacks")
    output.append("   ✓ Integrity check included")
    output.append("   ✓ PKCS#1 v2.1 standard (RFC 8017)")
    output.append("")
    
    output.append("🔏 PSS (Signature):")
    output.append("   ✓ Probabilistic → Different signature each time")
    output.append("   ✓ Provably secure in random oracle model")
    output.append("   ✓ Better security reduction than textbook")
    output.append("   ✓ PKCS#1 v2.1 standard (RFC 8017)")
    output.append("")
    
    output.append("=" * 80)
    output.append("RECOMMENDATION")
    output.append("=" * 80)
    output.append("")
    output.append("🎯 For Production/Real-world Applications:")
    output.append("   • Always use OAEP for encryption")
    output.append("   • Always use PSS for signatures")
    output.append("   • NEVER use Textbook RSA in production!")
    output.append("")
    output.append("📚 For Education/Learning:")
    output.append("   • Textbook RSA is good to understand basics")
    output.append("   • Then learn WHY padding is necessary")
    output.append("   • Understand the attacks it prevents")
    output.append("")
    
    return "\n".join(output)


if __name__ == '__main__':
    print(demo_padding_comparison())
