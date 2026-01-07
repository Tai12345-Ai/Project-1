import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import secrets
from Algorithms.rsa import keygen, RSA


def main():
    print("=== DEMO 05: Textbook RSA is deterministic (padding note) ===\n")
    print("Problem: Textbook RSA is deterministic")
    print("  - Same plaintext -> Same ciphertext")
    print("  - Vulnerable to: known-plaintext, chosen-plaintext attacks")
    print("  - Attacker can build a dictionary of ciphertexts\n")
    
    pub, priv = keygen(bits=512)
    rsa = RSA(pub=pub, priv=priv)
    pub_only = RSA(pub=pub, priv=None)

    print("=" * 70)
    print("Part 1: Demonstrating the problem")
    print("=" * 70)
    
    message = b"same message"
    print(f"\nOriginal message: {message}")
    print("Encrypting the same message twice...\n")

    c1 = pub_only.encrypt_bytes(message)
    c2 = pub_only.encrypt_bytes(message)

    print(f"Ciphertext #1: {c1}")
    print(f"Ciphertext #2: {c2}")
    print(f"\n❌ Same ciphertext? {c1 == c2}")
    
    if c1 == c2:
        print("\nThis is a SECURITY VULNERABILITY!")
        print("  - Attacker can detect if same message was sent twice")
        print("  - Attacker can build dictionary: message -> ciphertext")
        print("  - Example: 'YES' and 'NO' votes could be distinguished")

    print("\n" + "=" * 70)
    print("Part 2: Real-world solutions (not implemented here)")
    print("=" * 70)
    print("\nStandard padding schemes:")
    print("  1. PKCS#1 v1.5 (older, still used)")
    print("     - Adds random padding before encryption")
    print("     - Format: 0x00 || 0x02 || random || 0x00 || message")
    print("\n  2. OAEP (Optimal Asymmetric Encryption Padding)")
    print("     - Modern standard (RSA-OAEP)")
    print("     - Uses hash functions + MGF (Mask Generation Function)")
    print("     - Provably secure under random oracle model")
    print("     - Prevents chosen-ciphertext attacks")
    print("\n  3. RSA-PSS (for signatures)")
    print("     - Probabilistic Signature Scheme")
    print("     - Makes signatures randomized")
    
    print("\nNote: These are NOT covered in CLRS Ch. 31 (focuses on math)")
    print("      But they are ESSENTIAL for real-world RSA!")

    print("\n" + "=" * 70)
    print("Part 3: Simple randomization demo (NOT a real padding scheme)")
    print("=" * 70)
    print("\nAdding random salt to show concept (this is NOT OAEP!):\n")

    # Demo "randomized wrapper" đơn giản (KHÔNG phải OAEP)
    salt1 = secrets.token_bytes(16)
    salt2 = secrets.token_bytes(16)
    
    wrapped1 = salt1 + message
    wrapped2 = salt2 + message
    
    print(f"Salt #1: {salt1.hex()}")
    print(f"Wrapped message #1: salt1 + message")
    print(f"Salt #2: {salt2.hex()}")
    print(f"Wrapped message #2: salt2 + message\n")
    
    c3 = pub_only.encrypt_bytes(wrapped1)
    c4 = pub_only.encrypt_bytes(wrapped2)
    
    print(f"Ciphertext #3: {c3}")
    print(f"Ciphertext #4: {c4}")
    print(f"\n✓ Same ciphertext now? {c3 == c4}")
    
    if c3 != c4:
        print("\nWith randomization, same message produces different ciphertexts!")
        print("This is the basic idea behind padding schemes.")
    
    # Decrypt to verify
    dec3 = rsa.decrypt_bytes(c3)
    dec4 = rsa.decrypt_bytes(c4)
    
    print(f"\nDecrypted #3 (with salt): {dec3}")
    print(f"Decrypted #4 (with salt): {dec4}")
    print(f"Original message in both: {message in dec3 and message in dec4}")

    print("\n" + "=" * 70)
    print("Attack scenarios prevented by proper padding:")
    print("=" * 70)
    print("  1. Chosen-plaintext attack")
    print("     - Attacker encrypts guesses and compares ciphertexts")
    print("     - Example: Guess password, compare with intercepted ciphertext")
    print("\n  2. Dictionary attack")
    print("     - Pre-compute ciphertext for common messages")
    print("     - Example: 'Yes' / 'No' votes, common passwords")
    print("\n  3. Traffic analysis")
    print("     - Identify when same message is sent multiple times")
    print("     - Example: Repeated commands, recurring transactions")
    
    print("\n" + "=" * 70)
    print("Summary:")
    print("=" * 70)
    print("  ❌ Never use textbook RSA in production!")
    print("  ✓ Always use proper padding (OAEP for encryption)")
    print("  ✓ Use established libraries (e.g., cryptography.io)")
    print("  ✓ This demo is for LEARNING ONLY")
    print("=" * 70)


if __name__ == "__main__":
    main()