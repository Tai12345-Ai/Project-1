"""
Demo 07: Key Size and Security
Analysis of RSA key sizes and performance
"""
from .demo_utils import *

def demo_key_size_security():
    """Demo 07: Key size and security analysis"""
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 22 + "DEMO 07: RSA KEY SIZE & SECURITY" + " " * 24 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    
    print("=" * 80)
    print("RSA KEY SIZE RECOMMENDATIONS")
    print("=" * 80)
    print("""
┌──────────────┬────────────────┬──────────────────┬─────────────────────┐
│  Key Size    │  Symmetric     │  Status          │  Usage              │
│  (bits)      │  Equivalent    │                  │                     │
├──────────────┼────────────────┼──────────────────┼─────────────────────┤
│  512         │  ~56-bit       │  ✗ BROKEN        │  Never use          │
│  768         │  ~64-bit       │  ✗ BROKEN        │  Never use          │
│  1024        │  ~80-bit       │  ⚠️  DEPRECATED   │  Legacy only        │
│  2048        │  ~112-bit      │  ✓ SECURE        │  Recommended        │
│  3072        │  ~128-bit      │  ✓ SECURE        │  High security      │
│  4096        │  ~140-bit      │  ✓ SECURE        │  Maximum security   │
└──────────────┴────────────────┴──────────────────┴─────────────────────┘

Standards:
• NIST: Minimum 2048-bit (2023+)
• ENISA: 3072-bit for protection beyond 2030
• BSI: 3000-bit minimum for high security
""")
    
    # Performance comparison
    print("=" * 80)
    print("PERFORMANCE COMPARISON")
    print("=" * 80)
    
    key_sizes = [512, 1024, 2048]
    
    print(f"\n{'Operation':<20} {'512-bit':<15} {'1024-bit':<15} {'2048-bit':<15}")
    print("-" * 80)
    
    results = {}
    
    for bits in key_sizes:
        print(f"\nGenerating {bits}-bit key...")
        
        # Key generation
        t0 = time.perf_counter()
        pub, priv = keygen(bits=bits)
        t1 = time.perf_counter()
        keygen_time = (t1 - t0) * 1000
        
        rsa = RSA(pub=pub, priv=priv)
        pub_only = RSA(pub=pub, priv=None)
        
        # Encryption
        msg = b"Test message for performance"
        t0 = time.perf_counter()
        c = pub_only.encrypt_bytes(msg)
        t1 = time.perf_counter()
        encrypt_time = (t1 - t0) * 1000
        
        # Decryption
        t0 = time.perf_counter()
        rsa.decrypt_bytes(c)
        t1 = time.perf_counter()
        decrypt_time = (t1 - t0) * 1000
        
        # Signing
        t0 = time.perf_counter()
        sig = rsa.sign(msg)
        t1 = time.perf_counter()
        sign_time = (t1 - t0) * 1000
        
        # Verify
        t0 = time.perf_counter()
        pub_only.verify(msg, sig)
        t1 = time.perf_counter()
        verify_time = (t1 - t0) * 1000
        
        results[bits] = {
            'keygen': keygen_time,
            'encrypt': encrypt_time,
            'decrypt': decrypt_time,
            'sign': sign_time,
            'verify': verify_time
        }
    
    # Display results
    for op in ['keygen', 'encrypt', 'decrypt', 'sign', 'verify']:
        op_name = op.capitalize()
        row = f"{op_name:<20}"
        for bits in key_sizes:
            row += f" {results[bits][op]:<14.2f}"
        print(row)
    
    print("\n(All times in milliseconds)")
    
    # Security timeline
    print("\n" + "=" * 80)
    print("HISTORICAL TIMELINE")
    print("=" * 80)
    print("""
1977: RSA invented (512-bit considered secure)
1994: 129-digit (428-bit) RSA factored
1999: 512-bit RSA factored (project took months)
2009: 768-bit RSA factored (2 years of computation)
2020: 829-bit (250-digit) RSA factored
2023: 1024-bit still standing, but deprecated

Future threats:
📅 2030+: 2048-bit may become vulnerable
🔮 Quantum computing: All current RSA at risk
    → Need post-quantum cryptography
""")
    
    print("✅ Demo 07 completed!")
