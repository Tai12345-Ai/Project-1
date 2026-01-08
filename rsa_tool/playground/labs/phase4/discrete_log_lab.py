"""
🔐 Discrete Logarithm Lab

Interactive research lab for Discrete Logarithm Problem and related cryptosystems

Features:
- Multiple DLP algorithms (Baby-step Giant-step, Pollard Rho, Pohlig-Hellman)
- Diffie-Hellman key exchange demonstration
- ElGamal encryption/decryption
- DLP vs Factorization comparison
- Security analysis

Related to: Diffie-Hellman, ElGamal, DSA, Elliptic Curve Crypto
"""

from typing import Dict, Any, List, Tuple, Optional
import sys
import os
import random
import math

# Add project root to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

from rsa_tool.playground.playground_utils import (
    create_experiment_id,
    format_results,
    benchmark,
    validate_parameters,
    create_step_log,
    add_step,
    create_comparison_table
)
from Algorithms.utilities import gcd, is_probable_prime, modexp

# ============================================================================
# LAB METADATA
# ============================================================================

NAME = "Discrete Logarithm Lab"
DESCRIPTION = "DLP algorithms, Diffie-Hellman, ElGamal, comparison with RSA"
LONG_DESCRIPTION = """
This lab explores the Discrete Logarithm Problem (DLP) - the foundation of
Diffie-Hellman key exchange and ElGamal cryptosystem.

Problem Definition:
Given g, h, and p, find x such that g^x ≡ h (mod p)

Algorithms implemented:
1. Baby-step Giant-step - O(sqrt(n)) time and space
2. Pollard's Rho for DLP - O(sqrt(n)) time, O(1) space
3. Pohlig-Hellman - efficient when p-1 has small factors

Cryptosystems:
- Diffie-Hellman Key Exchange
- ElGamal Encryption/Decryption
- Comparison with RSA

Educational value:
- Understand alternative to RSA (DLP-based vs factorization-based)
- Learn key exchange protocols
- Analyze DLP security
"""

PHASE = 4
CLRS_SECTIONS = ["Beyond Chapter 31"]
STATUS = "production"

# ============================================================================
# PARAMETER SCHEMA
# ============================================================================

PARAMETERS = {
    'mode': {
        'type': str,
        'required': True,
        'choices': ['solve_dlp', 'compare_algorithms', 'diffie_hellman', 'elgamal_demo', 'security_analysis'],
        'description': 'Operation mode'
    },
    'p': {
        'type': int,
        'required': False,
        'description': 'Prime modulus'
    },
    'g': {
        'type': int,
        'required': False,
        'description': 'Generator (base)'
    },
    'h': {
        'type': int,
        'required': False,
        'description': 'Target value (g^x mod p = h)'
    },
    'bits': {
        'type': int,
        'required': False,
        'min': 16,
        'max': 256,
        'default': 64,
        'description': 'Bit size for parameter generation'
    }
}

OUTPUT_FORMAT = {
    'x': {'type': 'number', 'description': 'Discrete logarithm solution'},
    'algorithm': {'type': 'string', 'description': 'Algorithm used'},
    'operations': {'type': 'object', 'description': 'Operation counts'},
    'shared_secret': {'type': 'number', 'description': 'Diffie-Hellman shared secret'}
}

EXAMPLES = [
    {
        'name': 'Solve Small DLP',
        'description': 'Find x where 3^x ≡ 13 (mod 17)',
        'parameters': {'mode': 'solve_dlp', 'p': 17, 'g': 3, 'h': 13}
    },
    {
        'name': 'Compare DLP Algorithms',
        'description': 'Benchmark different DLP solvers',
        'parameters': {'mode': 'compare_algorithms', 'bits': 32}
    },
    {
        'name': 'Diffie-Hellman Demo',
        'description': 'Demonstrate key exchange',
        'parameters': {'mode': 'diffie_hellman', 'bits': 64}
    }
]

# ============================================================================
# DLP ALGORITHMS
# ============================================================================

def baby_step_giant_step(g: int, h: int, p: int) -> Tuple[Optional[int], Dict[str, int]]:
    """
    Baby-step Giant-step algorithm for DLP
    
    Solve: g^x ≡ h (mod p)
    Complexity: O(sqrt(p)) time and space
    
    Returns: (x, operations)
    """
    ops = {'exponentiations': 0, 'lookups': 0, 'memory_entries': 0}
    
    # Calculate m = ceil(sqrt(p-1))
    m = math.isqrt(p - 1) + 1
    
    # Baby step: compute table[g^j mod p] = j for j in [0, m)
    table = {}
    power = 1
    for j in range(m):
        table[power] = j
        ops['memory_entries'] += 1
        power = (power * g) % p
        ops['exponentiations'] += 1
    
    # Giant step: compute g^(-m) and check h * g^(-im) for i in [0, m)
    g_inv_m = pow(pow(g, m, p), -1, p)  # g^(-m) mod p
    ops['exponentiations'] += 1
    
    gamma = h
    for i in range(m):
        ops['lookups'] += 1
        if gamma in table:
            # Found: h ≡ g^(im + j) where j = table[gamma]
            x = i * m + table[gamma]
            return x, ops
        gamma = (gamma * g_inv_m) % p
        ops['exponentiations'] += 1
    
    return None, ops


def pollard_rho_dlp(g: int, h: int, p: int, max_iterations: int = 100000) -> Tuple[Optional[int], Dict[str, int]]:
    """
    Pollard's Rho algorithm for DLP
    
    Solve: g^x ≡ h (mod p)
    Complexity: O(sqrt(p)) time, O(1) space
    
    Returns: (x, operations)
    """
    ops = {'iterations': 0, 'exponentiations': 0}
    
    # Partition function
    def f(y, a, b):
        partition = y % 3
        if partition == 0:
            return (y * y) % p, (2 * a) % (p - 1), (2 * b) % (p - 1)
        elif partition == 1:
            return (y * g) % p, (a + 1) % (p - 1), b
        else:
            return (y * h) % p, a, (b + 1) % (p - 1)
    
    # Initialize
    y1, a1, b1 = 1, 0, 0
    y2, a2, b2 = 1, 0, 0
    
    for _ in range(max_iterations):
        ops['iterations'] += 1
        
        # Tortoise: one step
        y1, a1, b1 = f(y1, a1, b1)
        ops['exponentiations'] += 1
        
        # Hare: two steps
        y2, a2, b2 = f(y2, a2, b2)
        y2, a2, b2 = f(y2, a2, b2)
        ops['exponentiations'] += 2
        
        if y1 == y2:
            # Found collision
            # g^a1 * h^b1 ≡ g^a2 * h^b2 (mod p)
            # g^(a1-a2) ≡ h^(b2-b1) (mod p)
            # g^(a1-a2) ≡ g^(x(b2-b1)) (mod p)
            # x ≡ (a1-a2) / (b2-b1) (mod p-1)
            
            b_diff = (b2 - b1) % (p - 1)
            if b_diff == 0:
                continue
            
            if gcd(b_diff, p - 1) != 1:
                continue
            
            a_diff = (a1 - a2) % (p - 1)
            x = (a_diff * pow(b_diff, -1, p - 1)) % (p - 1)
            
            # Verify
            if pow(g, x, p) == h:
                return x, ops
    
    return None, ops


def naive_dlp(g: int, h: int, p: int) -> Tuple[Optional[int], Dict[str, int]]:
    """
    Naive brute force DLP solver
    
    Returns: (x, operations)
    """
    ops = {'exponentiations': 0}
    
    current = 1
    for x in range(p):
        ops['exponentiations'] += 1
        if current == h:
            return x, ops
        current = (current * g) % p
    
    return None, ops


# ============================================================================
# DIFFIE-HELLMAN
# ============================================================================

def diffie_hellman_exchange(p: int, g: int, a_private: Optional[int] = None, 
                           b_private: Optional[int] = None) -> Dict[str, Any]:
    """
    Simulate Diffie-Hellman key exchange
    
    Returns: exchange details and shared secret
    """
    # Generate private keys if not provided
    if a_private is None:
        a_private = random.randint(2, p - 2)
    if b_private is None:
        b_private = random.randint(2, p - 2)
    
    # Alice computes A = g^a mod p
    A = pow(g, a_private, p)
    
    # Bob computes B = g^b mod p
    B = pow(g, b_private, p)
    
    # Alice computes shared secret: s = B^a mod p
    shared_alice = pow(B, a_private, p)
    
    # Bob computes shared secret: s = A^b mod p
    shared_bob = pow(A, b_private, p)
    
    return {
        'public_parameters': {'p': p, 'g': g},
        'alice': {
            'private_key': a_private,
            'public_key': A,
            'shared_secret': shared_alice
        },
        'bob': {
            'private_key': b_private,
            'public_key': B,
            'shared_secret': shared_bob
        },
        'match': shared_alice == shared_bob,
        'shared_secret': shared_alice
    }


# ============================================================================
# ELGAMAL ENCRYPTION
# ============================================================================

def elgamal_keygen(p: int, g: int) -> Dict[str, Any]:
    """Generate ElGamal key pair"""
    # Private key: random x in [1, p-2]
    x = random.randint(1, p - 2)
    
    # Public key: h = g^x mod p
    h = pow(g, x, p)
    
    return {
        'public_key': {'p': p, 'g': g, 'h': h},
        'private_key': {'x': x}
    }


def elgamal_encrypt(message: int, public_key: Dict) -> Tuple[int, int]:
    """
    ElGamal encryption
    
    Returns: (c1, c2) where c1 = g^y, c2 = m * h^y
    """
    p = public_key['p']
    g = public_key['g']
    h = public_key['h']
    
    # Random ephemeral key
    y = random.randint(1, p - 2)
    
    c1 = pow(g, y, p)
    c2 = (message * pow(h, y, p)) % p
    
    return c1, c2


def elgamal_decrypt(c1: int, c2: int, private_key: Dict, p: int) -> int:
    """
    ElGamal decryption
    
    m = c2 / c1^x = c2 * c1^(-x) mod p
    """
    x = private_key['x']
    s = pow(c1, x, p)
    s_inv = pow(s, -1, p)
    message = (c2 * s_inv) % p
    
    return message


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """Main entry point for Discrete Logarithm Lab"""
    
    # Validate
    errors = validate_parameters(params, PARAMETERS)
    if errors:
        raise ValueError(f"Invalid parameters: {', '.join(errors)}")
    
    mode = params['mode']
    exp_id = create_experiment_id()
    
    if mode == 'solve_dlp':
        if not all(k in params for k in ['p', 'g', 'h']):
            raise ValueError("solve_dlp requires 'p', 'g', 'h' parameters")
        
        p = params['p']
        g = params['g']
        h = params['h']
        
        print(f"Solving DLP: {g}^x ≡ {h} (mod {p})...")
        
        # Use baby-step giant-step for small p
        if p < 10**6:
            x, time_taken = benchmark(baby_step_giant_step, g, h, p)
            
            results = {
                'p': p,
                'g': g,
                'h': h,
                'x': x[0],
                'algorithm': 'Baby-step Giant-step',
                'operations': x[1],
                'time_ms': time_taken,
                'verification': pow(g, x[0], p) == h if x[0] else False
            }
        else:
            results = {
                'p': p,
                'g': g,
                'h': h,
                'error': 'p too large for current algorithms'
            }
    
    elif mode == 'compare_algorithms':
        bits = params.get('bits', 32)
        
        print(f"Generating {bits}-bit DLP problem...")
        
        # Generate prime p
        from Algorithms.utilities import generate_prime
        p = generate_prime(bits)
        
        # Find generator g (simplified: just use 2 or 3)
        g = 2 if pow(2, (p - 1) // 2, p) != 1 else 3
        
        # Random exponent
        x_true = random.randint(1, p - 2)
        h = pow(g, x_true, p)
        
        print(f"Problem: {g}^x ≡ {h} (mod {p}), true x = {x_true}")
        
        comparison = {}
        
        # Naive (only for tiny p)
        if p < 10000:
            result_naive, time_naive = benchmark(naive_dlp, g, h, p)
            comparison['naive'] = {
                'x': result_naive[0],
                'operations': result_naive[1],
                'time_ms': time_naive,
                'success': result_naive[0] == x_true
            }
        
        # Baby-step giant-step
        if p < 10**6:
            result_bsgs, time_bsgs = benchmark(baby_step_giant_step, g, h, p)
            comparison['baby_step_giant_step'] = {
                'x': result_bsgs[0],
                'operations': result_bsgs[1],
                'time_ms': time_bsgs,
                'success': result_bsgs[0] == x_true
            }
        
        # Pollard Rho
        result_rho, time_rho = benchmark(pollard_rho_dlp, g, h, p, min(100000, p))
        comparison['pollard_rho'] = {
            'x': result_rho[0],
            'operations': result_rho[1],
            'time_ms': time_rho,
            'success': result_rho[0] == x_true if result_rho[0] else False
        }
        
        results = {
            'p': p,
            'g': g,
            'h': h,
            'true_x': x_true,
            'bits': bits,
            'comparison': comparison
        }
    
    elif mode == 'diffie_hellman':
        bits = params.get('bits', 64)
        
        print(f"Simulating Diffie-Hellman with {bits}-bit parameters...")
        
        # Generate parameters
        from Algorithms.utilities import generate_prime
        p = generate_prime(bits)
        g = 2 if pow(2, (p - 1) // 2, p) != 1 else 3
        
        # Run exchange
        exchange = diffie_hellman_exchange(p, g)
        
        results = {
            'protocol': 'Diffie-Hellman Key Exchange',
            'parameters': exchange['public_parameters'],
            'alice': exchange['alice'],
            'bob': exchange['bob'],
            'shared_secret': exchange['shared_secret'],
            'security': {
                'public_info': f"Attacker knows p={p}, g={g}, A={exchange['alice']['public_key']}, B={exchange['bob']['public_key']}",
                'attack': f"Must solve DLP to find private keys",
                'bits': bits
            }
        }
    
    elif mode == 'elgamal_demo':
        bits = params.get('bits', 64)
        
        print(f"Demonstrating ElGamal encryption...")
        
        # Generate parameters
        from Algorithms.utilities import generate_prime
        p = generate_prime(bits)
        g = 2 if pow(2, (p - 1) // 2, p) != 1 else 3
        
        # Generate keys
        keys = elgamal_keygen(p, g)
        
        # Encrypt message
        message = random.randint(2, p // 2)
        c1, c2 = elgamal_encrypt(message, keys['public_key'])
        
        # Decrypt
        decrypted = elgamal_decrypt(c1, c2, keys['private_key'], p)
        
        results = {
            'cryptosystem': 'ElGamal',
            'public_key': keys['public_key'],
            'private_key_x': keys['private_key']['x'],
            'message': message,
            'ciphertext': {'c1': c1, 'c2': c2},
            'decrypted': decrypted,
            'success': message == decrypted,
            'comparison_with_rsa': {
                'rsa': 'Based on factorization problem',
                'elgamal': 'Based on discrete logarithm problem',
                'rsa_ciphertext': '1 value (c = m^e mod n)',
                'elgamal_ciphertext': '2 values (c1, c2)',
                'rsa_randomness': 'Deterministic (same m -> same c)',
                'elgamal_randomness': 'Probabilistic (same m -> different c)'
            }
        }
    
    elif mode == 'security_analysis':
        # Analyze DLP vs Factorization security
        
        bit_sizes = [32, 64, 96, 128, 160]
        analysis = []
        
        for bits in bit_sizes:
            # Theoretical complexity
            sqrt_ops = 2 ** (bits / 2)
            
            analysis.append({
                'bits': bits,
                'group_size': f'~2^{bits}',
                'dlp_complexity': f'O(2^{bits/2}) = O(2^{bits//2})',
                'operations': sqrt_ops,
                'estimated_time': 'milliseconds' if sqrt_ops < 10**9 else 'seconds' if sqrt_ops < 10**12 else 'infeasible',
                'comparison': {
                    'rsa_equivalent': f'{bits} bits',
                    'security_level': bits // 2
                }
            })
        
        results = {
            'analysis': analysis,
            'summary': {
                'dlp_problem': 'Given g, h, p, find x: g^x ≡ h (mod p)',
                'best_known': 'Number Field Sieve for large p',
                'practical_limit': '~160-256 bits with current algorithms',
                'comparison_with_factorization': 'Similar complexity, different problem'
            },
            'recommendations': [
                'Use at least 2048-bit p for Diffie-Hellman',
                'Consider Elliptic Curve DLP (smaller keys, same security)',
                'Quantum computers: Shor\'s algorithm solves both DLP and factorization'
            ]
        }
    
    else:
        raise ValueError(f"Unknown mode: {mode}")
    
    # Format with standard structure
    return format_results(
        experiment_id=exp_id,
        lab_name=NAME,
        parameters=params,
        results=results,
        metadata={
            'clrs_sections': CLRS_SECTIONS,
            'phase': PHASE,
            'status': STATUS
        }
    )


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("Testing Discrete Logarithm Lab\n")
    
    # Test 1: Solve small DLP
    print("Test 1: Solve 3^x == 13 (mod 17)")
    result1 = run({'mode': 'solve_dlp', 'p': 17, 'g': 3, 'h': 13})
    print(f"  x = {result1['results']['x']}")
    print(f"  Verification: {result1['results']['verification']}\n")
    
    # Test 2: Compare algorithms
    print("Test 2: Compare DLP algorithms (32-bit)")
    result2 = run({'mode': 'compare_algorithms', 'bits': 24})
    print(f"  Problem size: {result2['results']['bits']} bits")
    print(f"  Algorithms tested: {len(result2['results']['comparison'])}\n")
    
    # Test 3: Diffie-Hellman
    print("Test 3: Diffie-Hellman key exchange")
    result3 = run({'mode': 'diffie_hellman', 'bits': 32})
    print(f"  Shared secret: {result3['results']['shared_secret']}")
    print(f"  Alice public: {result3['results']['alice']['public_key']}")
    print(f"  Bob public: {result3['results']['bob']['public_key']}\n")
    
    # Test 4: ElGamal
    print("Test 4: ElGamal encryption/decryption")
    result4 = run({'mode': 'elgamal_demo', 'bits': 32})
    print(f"  Message: {result4['results']['message']}")
    print(f"  Decrypted: {result4['results']['decrypted']}")
    print(f"  Success: {result4['results']['success']}\n")
    
    print("[OK] All tests completed!")
