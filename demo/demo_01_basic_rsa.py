import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Algorithms.rsa import keygen, RSA


def main():
    print("=== DEMO 01: Basic RSA encrypt/decrypt + signature ===\n")
    
    # Keygen for Alice and Bob
    pub_a, priv_a = keygen(bits=512)   # đổi 1024 nếu muốn mạnh hơn
    pub_b, priv_b = keygen(bits=512)

    # Show Alice's RSA parameters (CLRS 31.7)
    print("Alice's RSA key parameters:")
    print(f"  Public key (e, n):")
    print(f"    e = {pub_a.e}")
    print(f"    n = {pub_a.n} ({pub_a.n.bit_length()} bits)")
    print(f"  Private key (d, n):")
    print(f"    d = {priv_a.d}")
    print(f"    p = {priv_a.p} ({priv_a.p.bit_length()} bits)")
    print(f"    q = {priv_a.q} ({priv_a.q.bit_length()} bits)")
    print(f"    n = p * q = {priv_a.p * priv_a.q == pub_a.n}\n")

    # RSA objects
    alice = RSA(pub=pub_a, priv=priv_a)
    bob = RSA(pub=pub_b, priv=priv_b)

    # pub_only: dùng khi chỉ có public key (encrypt/verify only, không decrypt/sign)
    alice_pub_only = RSA(pub=pub_a, priv=None)
    bob_pub_only = RSA(pub=pub_b, priv=None)

    msg_from_bob = "Hello Alice! This is Bob."
    msg_from_alice = "Hello Bob!"

    # ---- Encryption Demo ----
    print("=" * 60)
    print("Encryption Demo: Bob -> Alice")
    print("=" * 60)
    
    # Bob encrypts with Alice's public key (only Alice can decrypt)
    c1 = alice_pub_only.encrypt_text(msg_from_bob)
    print(f"Original message: '{msg_from_bob}'")
    print(f"Ciphertext blocks: {c1}")
    print(f"Number of blocks: {len(c1)}")
    
    # Alice decrypts with her private key
    p1 = alice.decrypt_text(c1)
    print(f"Alice decrypted: '{p1}'")
    print(f"Decryption successful: {p1 == msg_from_bob}\n")

    # Alice -> Bob
    print("=" * 60)
    print("Encryption Demo: Alice -> Bob")
    print("=" * 60)
    c2 = bob_pub_only.encrypt_text(msg_from_alice)
    print(f"Original message: '{msg_from_alice}'")
    print(f"Ciphertext blocks: {c2}")
    p2 = bob.decrypt_text(c2)
    print(f"Bob decrypted: '{p2}'")
    print(f"Decryption successful: {p2 == msg_from_alice}\n")

    # ---- Digital Signature Demo ----
    print("=" * 60)
    print("Digital Signature Demo (Textbook RSA)")
    print("=" * 60)
    
    # Bob signs his message with his private key
    sig_b = bob.sign(msg_from_bob.encode("utf-8"))
    print(f"Bob's message: '{msg_from_bob}'")
    print(f"Bob's signature: {sig_b}")
    
    # Anyone with Bob's public key can verify
    ok_b = bob_pub_only.verify(msg_from_bob.encode("utf-8"), sig_b)
    print(f"Signature verified with Bob's public key: {ok_b}")
    
    # Tampered message verification
    tampered = "Hello Alice! This is Eve."
    ok_tampered = bob_pub_only.verify(tampered.encode("utf-8"), sig_b)
    print(f"Tampered message verification: {ok_tampered} (should be False)\n")

    # Alice signs her message
    sig_a = alice.sign(msg_from_alice.encode("utf-8"))
    ok_a = alice_pub_only.verify(msg_from_alice.encode("utf-8"), sig_a)
    print(f"Alice's message: '{msg_from_alice}'")
    print(f"Alice's signature: {sig_a}")
    print(f"Signature verified with Alice's public key: {ok_a}")

    print("\n" + "=" * 60)
    print("Summary:")
    print("  - Encryption: message^e mod n (anyone can encrypt)")
    print("  - Decryption: ciphertext^d mod n (only private key holder)")
    print("  - Signature: hash^d mod n (only private key holder)")
    print("  - Verify: signature^e mod n (anyone can verify)")
    print("=" * 60)


if __name__ == "__main__":
    main()