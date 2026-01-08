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
    
    # ---- Methods with padding support ----
    @staticmethod
    def encrypt_with_padding(message, e, n, padding_mode='textbook'):
        """
        Mã hóa message với lựa chọn padding mode
        
        Args:
            message: Text cần mã hóa
            e: Public exponent
            n: Modulus
            padding_mode: 'textbook' hoặc 'oaep'
            
        Returns:
            dict: {'ciphertext': ..., 'mode': ..., 'security_level': ...}
        """
        pub = PublicKey(e=e, n=n)
        rsa = RSA(pub=pub, priv=None)
        
        if padding_mode == 'oaep':
            ciphertext = rsa.encrypt_oaep(message.encode('utf-8'))
            security_info = {
                'mode': 'OAEP (RFC 8017)',
                'security_level': 'High - Non-deterministic, IND-CCA2',
                'padding_scheme': 'PKCS#1 v2.1'
            }
        else:  # textbook
            ciphertext = rsa.encrypt_text(message)
            security_info = {
                'mode': 'Textbook RSA',
                'security_level': 'Low - Deterministic, malleable (educational only)',
                'padding_scheme': 'None'
            }
        
        return {
            'ciphertext': ciphertext if isinstance(ciphertext, int) else ciphertext,
            **security_info
        }
    
    @staticmethod
    def decrypt_with_padding(ciphertext, d, n, padding_mode='textbook', p=None, q=None, use_crt=False):
        """
        Giải mã ciphertext với lựa chọn padding mode
        
        Args:
            ciphertext: Ciphertext cần giải mã
            d: Private exponent
            n: Modulus
            padding_mode: 'textbook' hoặc 'oaep'
            p, q: Prime factors (cho CRT)
            use_crt: Có dùng CRT không
            
        Returns:
            dict: {'plaintext': ..., 'mode': ..., 'security_level': ...}
        """
        pub = PublicKey(e=65537, n=n)
        priv = PrivateKey(d=d, n=n, p=p, q=q)
        rsa = RSA(pub=pub, priv=priv)
        
        if padding_mode == 'oaep':
            plaintext = rsa.decrypt_oaep(ciphertext, use_crt=use_crt).decode('utf-8')
            security_info = {
                'mode': 'OAEP (RFC 8017)',
                'security_level': 'High - Protected against padding oracle attacks',
                'padding_scheme': 'PKCS#1 v2.1'
            }
        else:  # textbook
            plaintext = rsa.decrypt_text([ciphertext] if isinstance(ciphertext, int) else ciphertext, use_crt=use_crt)
            security_info = {
                'mode': 'Textbook RSA',
                'security_level': 'Low - Vulnerable to chosen ciphertext attacks',
                'padding_scheme': 'None'
            }
        
        return {
            'plaintext': plaintext,
            **security_info
        }
    
    @staticmethod
    def sign_with_padding(message, d, n, padding_mode='textbook'):
        """
        Ký số message với lựa chọn padding mode
        
        Args:
            message: Text cần ký
            d: Private exponent
            n: Modulus
            padding_mode: 'textbook' hoặc 'pss'
            
        Returns:
            dict: {'signature': ..., 'mode': ..., 'security_level': ...}
        """
        pub = PublicKey(e=65537, n=n)
        priv = PrivateKey(d=d, n=n)
        rsa = RSA(pub=pub, priv=priv)
        
        if padding_mode == 'pss':
            signature = rsa.sign_pss(message.encode('utf-8'))
            security_info = {
                'mode': 'PSS (RFC 8017)',
                'security_level': 'High - Probabilistic, provably secure',
                'padding_scheme': 'PKCS#1 v2.1'
            }
        else:  # textbook
            signature = rsa.sign(message.encode('utf-8'))
            security_info = {
                'mode': 'Textbook RSA Signature',
                'security_level': 'Low - Vulnerable to forgery attacks',
                'padding_scheme': 'None'
            }
        
        return {
            'signature': signature,
            **security_info
        }
    
    @staticmethod
    def verify_with_padding(message, signature, e, n, padding_mode='textbook'):
        """
        Xác minh chữ ký với lựa chọn padding mode
        
        Args:
            message: Text gốc
            signature: Chữ ký cần verify
            e: Public exponent
            n: Modulus
            padding_mode: 'textbook' hoặc 'pss'
            
        Returns:
            dict: {'valid': ..., 'mode': ..., 'security_level': ...}
        """
        pub = PublicKey(e=e, n=n)
        rsa = RSA(pub=pub, priv=None)
        
        if padding_mode == 'pss':
            valid = rsa.verify_pss(message.encode('utf-8'), signature)
            security_info = {
                'mode': 'PSS (RFC 8017)',
                'security_level': 'High - Provably secure verification',
                'padding_scheme': 'PKCS#1 v2.1'
            }
        else:  # textbook
            valid = rsa.verify(message.encode('utf-8'), signature)
            security_info = {
                'mode': 'Textbook RSA Verification',
                'security_level': 'Low - Susceptible to signature forgery',
                'padding_scheme': 'None'
            }
        
        return {
            'valid': valid,
            **security_info
        }
