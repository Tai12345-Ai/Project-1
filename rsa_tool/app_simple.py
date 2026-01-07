"""
RSA Cryptography Tool - Simplified Single File Version
All-in-one application for easy deployment
"""
from flask import Flask, render_template, request, jsonify
import sys
import os
import io
from contextlib import redirect_stdout
import time
import secrets

# Add parent directory to path to import Algorithms
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Algorithms.rsa import keygen, RSA, PublicKey, PrivateKey
from Algorithms.utilities import is_probable_prime, generate_prime, gcd, modinv
from Algorithms.pollard_rho import factor_semiprime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
app.config['DEBUG'] = True

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/key/generate', methods=['POST'])
def generate_key():
    """Generate RSA key pair"""
    try:
        data = request.json or {}
        bits = int(data.get('bits', 1024))
        e = int(data.get('e', 65537))
        
        if bits < 512 or bits > 4096:
            raise ValueError("Key size must be between 512 and 4096 bits")
        
        pub, priv = keygen(bits=bits, e=e)
        
        return jsonify({
            'success': True,
            'data': {
                'public_key': {
                    'e': str(pub.e),
                    'n': str(pub.n),
                    'n_bits': pub.n.bit_length()
                },
                'private_key': {
                    'd': str(priv.d),
                    'n': str(priv.n),
                    'p': str(priv.p),
                    'q': str(priv.q),
                    'p_bits': priv.p.bit_length(),
                    'q_bits': priv.q.bit_length()
                }
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/crypto/encrypt', methods=['POST'])
def encrypt():
    """Encrypt message"""
    try:
        data = request.json
        message = data.get('message', '')
        e = int(data.get('e'))
        n = int(data.get('n'))
        
        pub = PublicKey(e=e, n=n)
        rsa = RSA(pub=pub, priv=None)
        ciphertext_blocks = rsa.encrypt_text(message)
        
        return jsonify({
            'success': True,
            'data': {
                'ciphertext': [str(c) for c in ciphertext_blocks],
                'num_blocks': len(ciphertext_blocks),
                'original_length': len(message)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/crypto/decrypt', methods=['POST'])
def decrypt():
    """Decrypt ciphertext"""
    try:
        data = request.json
        ciphertext = [int(c) for c in data.get('ciphertext', [])]
        d = int(data.get('d'))
        n = int(data.get('n'))
        p = int(data.get('p', 0)) or None
        q = int(data.get('q', 0)) or None
        use_crt = data.get('use_crt', False)
        
        pub = PublicKey(e=65537, n=n)
        
        if p and q and use_crt:
            dp = d % (p - 1)
            dq = d % (q - 1)
            qinv = modinv(q, p)
            priv = PrivateKey(d=d, n=n, p=p, q=q, dp=dp, dq=dq, qinv=qinv)
        else:
            priv = PrivateKey(d=d, n=n)
        
        rsa = RSA(pub=pub, priv=priv)
        
        start_time = time.perf_counter()
        plaintext = rsa.decrypt_text(ciphertext)
        end_time = time.perf_counter()
        
        return jsonify({
            'success': True,
            'data': {
                'plaintext': plaintext,
                'use_crt': use_crt,
                'time_ms': (end_time - start_time) * 1000 if use_crt else None
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/crypto/sign', methods=['POST'])
def sign():
    """Sign message"""
    try:
        data = request.json
        message = data.get('message', '')
        d = int(data.get('d'))
        n = int(data.get('n'))
        
        pub = PublicKey(e=65537, n=n)
        priv = PrivateKey(d=d, n=n)
        rsa = RSA(pub=pub, priv=priv)
        
        signature = rsa.sign(message.encode('utf-8'))
        
        return jsonify({
            'success': True,
            'data': {'signature': str(signature)}
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/crypto/verify', methods=['POST'])
def verify():
    """Verify signature"""
    try:
        data = request.json
        message = data.get('message', '')
        signature = int(data.get('signature'))
        e = int(data.get('e'))
        n = int(data.get('n'))
        
        pub = PublicKey(e=e, n=n)
        rsa = RSA(pub=pub, priv=None)
        
        valid = rsa.verify(message.encode('utf-8'), signature)
        
        return jsonify({
            'success': True,
            'data': {'valid': valid}
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/demo/<demo_name>', methods=['GET'])
def run_demo(demo_name):
    """Run demonstration"""
    try:
        output = io.StringIO()
        
        with redirect_stdout(output):
            if demo_name == 'basic_rsa':
                demo_basic_rsa()
            elif demo_name == 'miller_rabin':
                demo_miller_rabin()
            elif demo_name == 'crt_speed':
                demo_crt_speed()
            elif demo_name == 'pollard_rho':
                demo_pollard_rho()
            elif demo_name == 'textbook_padding':
                demo_textbook_padding()
            else:
                return jsonify({'success': False, 'error': 'Unknown demo'}), 400
        
        return jsonify({
            'success': True,
            'data': {'output': output.getvalue()}
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== DEMO FUNCTIONS ====================

def demo_basic_rsa():
    print("=== DEMO 01: Basic RSA ===\n")
    pub_a, priv_a = keygen(bits=512)
    pub_b, priv_b = keygen(bits=512)
    
    alice = RSA(pub=pub_a, priv=priv_a)
    bob = RSA(pub=pub_b, priv=priv_b)
    
    print(f"Alice's key: n = {pub_a.n.bit_length()} bits\n")
    
    msg = "Hello Alice!"
    print(f"Message: '{msg}'")
    
    c = alice.encrypt_text(msg)
    print(f"Encrypted blocks: {len(c)}")
    
    p = alice.decrypt_text(c)
    print(f"Decrypted: '{p}'")
    print(f"Match: {p == msg}\n")
    
    # Signature
    sig_msg = "I owe Alice $100".encode()
    sig = bob.sign(sig_msg)
    print(f"\nSignature demo:")
    print(f"Message: {sig_msg.decode()}")
    print(f"Valid: {bob.verify(sig_msg, sig)}")

def demo_miller_rabin():
    print("=== DEMO 02: Miller-Rabin ===\n")
    tests = [(2, "prime"), (17, "prime"), (21, "composite"), (561, "Carmichael")]
    
    for n, desc in tests:
        result = is_probable_prime(n, rounds=20)
        status = "PRIME" if result else "COMPOSITE"
        print(f"{n:6d} -> {status:12s} ({desc})")
    
    print(f"\nGenerating 256-bit prime...")
    t0 = time.perf_counter()
    p = generate_prime(256, rounds=20)
    t1 = time.perf_counter()
    print(f"Generated: {str(p)[:50]}...")
    print(f"Time: {(t1-t0)*1000:.2f} ms")

def demo_crt_speed():
    print("=== DEMO 03: CRT Speed ===\n")
    pub, priv = keygen(bits=1024)
    rsa = RSA(pub=pub, priv=priv)
    
    message = ("CRT test " * 10).encode()
    c = rsa.encrypt_bytes(message)
    
    iterations = 10
    
    t0 = time.perf_counter()
    for _ in range(iterations):
        rsa.decrypt_bytes(c, use_crt=False)
    t1 = time.perf_counter()
    
    t2 = time.perf_counter()
    for _ in range(iterations):
        rsa.decrypt_bytes(c, use_crt=True)
    t3 = time.perf_counter()
    
    normal = t1 - t0
    crt = t3 - t2
    
    print(f"Normal: {normal:.4f}s")
    print(f"CRT:    {crt:.4f}s")
    if crt > 0:
        print(f"Speedup: {normal/crt:.2f}x")

def demo_pollard_rho():
    print("=== DEMO 04: Pollard Rho ===\n")
    bits = 96
    
    p = generate_prime(bits // 2, rounds=20)
    q = generate_prime(bits // 2, rounds=20)
    n = p * q
    
    print(f"Weak RSA ({bits} bits)")
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"n = {n}\n")
    
    print("Factoring...")
    t0 = time.perf_counter()
    pq = factor_semiprime(n)
    t1 = time.perf_counter()
    
    if pq:
        print(f"✓ Factored! Found p={pq[0]}, q={pq[1]}")
        print(f"Time: {(t1-t0)*1000:.2f} ms")
        print("RSA is broken!")

def demo_textbook_padding():
    print("=== DEMO 05: Textbook Padding ===\n")
    pub, priv = keygen(bits=512)
    rsa = RSA(pub=pub, priv=priv)
    
    msg = b"same message"
    c1 = rsa.encrypt_bytes(msg)
    c2 = rsa.encrypt_bytes(msg)
    
    print(f"Message: {msg}")
    print(f"Same ciphertext? {c1 == c2}")
    
    if c1 == c2:
        print("\n⚠️ SECURITY ISSUE!")
        print("- Deterministic encryption")
        print("- Vulnerable to attacks")
        print("- Use OAEP padding in practice")

# ==================== MAIN ====================

if __name__ == '__main__':
    print("Starting RSA Tool...")
    print("Open browser at: http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=True)
