"""
Shared utilities cho demos
"""
import sys
import os

# Add parent directory to import Algorithms
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Common imports for all demos
from Algorithms.rsa import keygen, RSA, PublicKey, PrivateKey
from Algorithms.utilities import is_probable_prime, generate_prime, modinv, gcd
from Algorithms.pollard_rho import factor_semiprime
import time
import secrets
import math
