"""
RSA Service - Business Logic Layer
Xử lý các thao tác RSA operations
"""
import sys
import os

# Add parent directory to import Algorithms
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Algorithms.rsa import keygen, RSA, PublicKey, PrivateKey
from Algorithms.utilities import modinv
import time

class RSAService:
    """
    Service xử lý các thao tác RSA
    
    Mục đích: Tách business logic ra khỏi routes
    """
    
    @staticmethod
    def generate_keys(bits=1024, e=65537):
        """
        Sinh cặp khóa RSA
        
        Args:
            bits: Độ dài key (512-4096)
            e: Public exponent
            
        Returns:
            dict: {'public_key': {...}, 'private_key': {...}}
        """
        pub, priv = keygen(bits=bits, e=e)
        
        return {
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
    
    @staticmethod
    def encrypt(message, e, n):
        """
        Mã hóa message bằng public key
        
        Args:
            message: Text cần mã hóa
            e: Public exponent
            n: Modulus
            
        Returns:
            dict: {'ciphertext': [...], 'num_blocks': int, ...}
        """
        pub = PublicKey(e=e, n=n)
        rsa = RSA(pub=pub, priv=None)
        ciphertext_blocks = rsa.encrypt_text(message)
        
        return {
            'ciphertext': [str(c) for c in ciphertext_blocks],
            'num_blocks': len(ciphertext_blocks),
            'original_length': len(message)
        }
    
    @staticmethod
    def decrypt(ciphertext, d, n, p=None, q=None, use_crt=False):
        """
        Giải mã ciphertext bằng private key
        
        Args:
            ciphertext: List of encrypted blocks
            d: Private exponent
            n: Modulus
            p, q: Primes (optional, for CRT)
            use_crt: Có dùng CRT optimization không
            
        Returns:
            dict: {'plaintext': str, 'use_crt': bool, 'time_ms': float}
        """
        pub = PublicKey(e=65537, n=n)
        
        # Tạo private key (có hoặc không CRT)
        if p and q and use_crt:
            dp = d % (p - 1)
            dq = d % (q - 1)
            qinv = modinv(q, p)
            priv = PrivateKey(d=d, n=n, p=p, q=q, dp=dp, dq=dq, qinv=qinv)
        else:
            priv = PrivateKey(d=d, n=n)
        
        rsa = RSA(pub=pub, priv=priv)
        
        # Đo thời gian nếu dùng CRT
        start = time.perf_counter()
        plaintext = rsa.decrypt_text(ciphertext)
        elapsed = time.perf_counter() - start
        
        return {
            'plaintext': plaintext,
            'use_crt': use_crt,
            'time_ms': elapsed * 1000 if use_crt else None
        }
    
    @staticmethod
    def sign(message, d, n):
        """
        Ký số message bằng private key
        
        Args:
            message: Text cần ký
            d: Private exponent
            n: Modulus
            
        Returns:
            int: Signature
        """
        pub = PublicKey(e=65537, n=n)
        priv = PrivateKey(d=d, n=n)
        rsa = RSA(pub=pub, priv=priv)
        
        return rsa.sign(message.encode('utf-8'))
    
    @staticmethod
    def verify(message, signature, e, n):
        """
        Xác minh chữ ký
        
        Args:
            message: Text gốc
            signature: Chữ ký cần verify
            e: Public exponent
            n: Modulus
            
        Returns:
            bool: True nếu hợp lệ
        """
        pub = PublicKey(e=e, n=n)
        rsa = RSA(pub=pub, priv=None)
        
        return rsa.verify(message.encode('utf-8'), signature)
