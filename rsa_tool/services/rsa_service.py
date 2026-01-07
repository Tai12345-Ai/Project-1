# rsa_tool/services/rsa_service.py
"""
RSA Service - Business logic for RSA operations
"""
import sys
import os
from typing import Tuple, List, Optional

# Add parent directories to path to import Algorithms
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from Algorithms.rsa import keygen, RSA, PublicKey, PrivateKey
from Algorithms.utilities import modinv
import time

# Import from parent package
import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from models import KeyPairResponse, EncryptResponse, DecryptResponse

class RSAService:
    """Service for RSA cryptographic operations"""
    
    @staticmethod
    def generate_keypair(bits: int = 1024, e: int = 65537) -> KeyPairResponse:
        """
        Generate RSA key pair
        
        Args:
            bits: Key size in bits
            e: Public exponent (default 65537)
            
        Returns:
            KeyPairResponse with public and private keys
        """
        pub, priv = keygen(bits=bits, e=e)
        
        public_key = {
            'e': str(pub.e),
            'n': str(pub.n),
            'n_bits': pub.n.bit_length()
        }
        
        private_key = {
            'd': str(priv.d),
            'n': str(priv.n),
            'p': str(priv.p),
            'q': str(priv.q),
            'p_bits': priv.p.bit_length(),
            'q_bits': priv.q.bit_length(),
            'dp': str(priv.dp) if priv.dp else None,
            'dq': str(priv.dq) if priv.dq else None,
            'qinv': str(priv.qinv) if priv.qinv else None
        }
        
        return KeyPairResponse(public_key=public_key, private_key=private_key)
    
    @staticmethod
    def encrypt_message(message: str, e: int, n: int) -> EncryptResponse:
        """
        Encrypt a message with RSA public key
        
        Args:
            message: Plaintext message
            e: Public exponent
            n: Modulus
            
        Returns:
            EncryptResponse with ciphertext blocks
        """
        pub = PublicKey(e=e, n=n)
        rsa = RSA(pub=pub, priv=None)
        
        ciphertext_blocks = rsa.encrypt_text(message)
        
        return EncryptResponse(
            ciphertext=[str(c) for c in ciphertext_blocks],
            num_blocks=len(ciphertext_blocks),
            original_length=len(message)
        )
    
    @staticmethod
    def decrypt_message(
        ciphertext: List[int], 
        d: int, 
        n: int,
        p: Optional[int] = None,
        q: Optional[int] = None,
        use_crt: bool = False
    ) -> DecryptResponse:
        """
        Decrypt a message with RSA private key
        
        Args:
            ciphertext: List of ciphertext blocks
            d: Private exponent
            n: Modulus
            p: Prime p (optional, for CRT)
            q: Prime q (optional, for CRT)
            use_crt: Whether to use CRT optimization
            
        Returns:
            DecryptResponse with plaintext
        """
        pub = PublicKey(e=65537, n=n)  # e doesn't matter for decryption
        
        # Create private key with or without CRT parameters
        if p and q and use_crt:
            dp = d % (p - 1)
            dq = d % (q - 1)
            qinv = modinv(q, p)
            priv = PrivateKey(d=d, n=n, p=p, q=q, dp=dp, dq=dq, qinv=qinv)
        else:
            priv = PrivateKey(d=d, n=n)
        
        rsa = RSA(pub=pub, priv=priv)
        
        # Measure time if using CRT
        start_time = time.perf_counter()
        plaintext = rsa.decrypt_text(ciphertext)
        end_time = time.perf_counter()
        
        time_ms = (end_time - start_time) * 1000 if use_crt else None
        
        return DecryptResponse(
            plaintext=plaintext,
            use_crt=use_crt,
            time_ms=time_ms
        )
    
    @staticmethod
    def sign_message(message: str, d: int, n: int) -> int:
        """
        Sign a message with RSA private key
        
        Args:
            message: Message to sign
            d: Private exponent
            n: Modulus
            
        Returns:
            Signature as integer
        """
        pub = PublicKey(e=65537, n=n)
        priv = PrivateKey(d=d, n=n)
        rsa = RSA(pub=pub, priv=priv)
        
        signature = rsa.sign(message.encode('utf-8'))
        return signature
    
    @staticmethod
    def verify_signature(message: str, signature: int, e: int, n: int) -> bool:
        """
        Verify RSA signature
        
        Args:
            message: Original message
            signature: Signature to verify
            e: Public exponent
            n: Modulus
            
        Returns:
            True if signature is valid, False otherwise
        """
        pub = PublicKey(e=e, n=n)
        rsa = RSA(pub=pub, priv=None)
        
        return rsa.verify(message.encode('utf-8'), signature)