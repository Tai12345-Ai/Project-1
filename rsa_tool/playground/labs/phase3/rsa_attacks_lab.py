"""
⚔️ RSA Attacks Lab

Interactive research lab for RSA cryptanalysis attacks

Features:
- Wiener's attack (small private exponent)
- Common modulus attack
- Broadcast attack (small public exponent)
- Håstad's broadcast attack
- Attack success analysis and mitigation

Based on: CLRS 31.7, real-world RSA vulnerabilities
"""

from typing import Dict, Any, List, Tuple, Optional
import sys
import os
import math

# Add project root to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')))

from rsa_tool.playground.playground_utils import (
    create_experiment_id,
    format_results,
    benchmark,
    validate_parameters,
    create_step_log,
    add_step
)
from Algorithms.rsa import keygen, RSA
from Algorithms.utilities import extended_gcd, gcd

# ============================================================================
# LAB METADATA
# ============================================================================

NAME = "RSA Attacks Lab"
DESCRIPTION = "RSA cryptanalysis: Wiener, Common Modulus, Broadcast attacks"
LONG_DESCRIPTION = """
This lab demonstrates various attacks on RSA implementations that use
weak parameters or improper usage patterns.

Attacks implemented:
1. Wiener's Attack - exploits small private exponent d
2. Common Modulus Attack - same n with different e values
3. Broadcast Attack - same message to multiple recipients with e=3
4. Håstad's Broadcast Attack - variation with linear padding

Educational purposes:
- Understand RSA vulnerabilities
- Learn secure parameter selection
- Analyze attack conditions
- Implement mitigation strategies

⚠️ For research and education only - do not use on real systems!
"""

PHASE = 3
CLRS_SECTIONS = ["31.7"]
STATUS = "production"

# ============================================================================
# PARAMETER SCHEMA
# ============================================================================

PARAMETERS = {
    'mode': {
        'type': str,
        'required': True,
        'choices': ['wiener_attack', 'common_modulus', 'broadcast_attack', 'attack_analysis'],
        'description': 'Attack type to demonstrate'
    },
    'bits': {
        'type': int,
        'required': False,
        'min': 256,
        'max': 2048,
        'default': 512,
        'description': 'RSA key size in bits'
    },
    'e': {
        'type': int,
        'required': False,
        'default': 3,
        'description': 'Public exponent (for relevant attacks)'
    },
    'message': {
        'type': int,
        'required': False,
        'description': 'Plaintext message for encryption attacks'
    }
}

OUTPUT_FORMAT = {
    'attack': {'type': 'string', 'description': 'Attack name'},
    'success': {'type': 'boolean', 'description': 'Attack succeeded'},
    'recovered': {'type': 'object', 'description': 'Recovered secrets'},
    'conditions': {'type': 'object', 'description': 'Attack conditions analysis'},
    'mitigation': {'type': 'array', 'description': 'Recommended mitigations'}
}

EXAMPLES = [
    {
        'name': 'Wiener Attack on Small d',
        'description': 'Attempt to recover small private exponent',
        'parameters': {'mode': 'wiener_attack', 'bits': 512}
    },
    {
        'name': 'Common Modulus Attack',
        'description': 'Recover message encrypted with same n, different e',
        'parameters': {'mode': 'common_modulus', 'bits': 512}
    },
    {
        'name': 'Broadcast Attack (e=3)',
        'description': 'Recover message sent to 3 recipients with e=3',
        'parameters': {'mode': 'broadcast_attack', 'bits': 512, 'e': 3}
    }
]

# ============================================================================
# WIENER'S ATTACK
# ============================================================================

def continued_fraction(n: int, e: int) -> List[Tuple[int, int]]:
    """
    Compute continued fraction convergents of e/n
    
    Returns: List of (k, d) candidates
    """
    convergents = []
    
    # Compute continued fraction expansion
    cf = []
    a, b = e, n
    while b:
        q = a // b
        cf.append(q)
        a, b = b, a - q * b
    
    # Compute convergents
    h_prev, k_prev = 1, 0
    h_curr, k_curr = cf[0], 1
    
    convergents.append((k_curr, h_curr))
    
    for i in range(1, min(len(cf), 100)):  # Limit iterations
        h_next = cf[i] * h_curr + h_prev
        k_next = cf[i] * k_curr + k_prev
        
        convergents.append((k_next, h_next))
        
        h_prev, k_prev = h_curr, k_curr
        h_curr, k_curr = h_next, k_next
    
    return convergents


def wiener_attack(n: int, e: int) -> Optional[int]:
    """
    Wiener's attack on RSA with small d
    
    Conditions: d < (1/3) * n^(1/4)
    
    Returns: private exponent d if found, None otherwise
    """
    convergents = continued_fraction(n, e)
    
    for k, d in convergents:
        if k == 0 or d == 0:
            continue
        
        # Check if e*d == 1 (mod phi(n))
        # If so, phi(n) = (e*d - 1) / k
        
        if (e * d - 1) % k != 0:
            continue
        
        phi_candidate = (e * d - 1) // k
        
        # Check if this phi gives valid p, q
        # n = p*q, phi = (p-1)(q-1) = n - (p+q) + 1
        # So: p + q = n - phi + 1
        
        p_plus_q = n - phi_candidate + 1
        discriminant = p_plus_q * p_plus_q - 4 * n
        
        if discriminant < 0:
            continue
        
        sqrt_disc = int(discriminant ** 0.5)
        if sqrt_disc * sqrt_disc != discriminant:
            continue
        
        p = (p_plus_q + sqrt_disc) // 2
        q = (p_plus_q - sqrt_disc) // 2
        
        if p * q == n and p > 1 and q > 1:
            # Verify d works
            if (e * d) % ((p - 1) * (q - 1)) == 1:
                return d
    
    return None


# ============================================================================
# COMMON MODULUS ATTACK
# ============================================================================

def common_modulus_attack(n: int, e1: int, e2: int, c1: int, c2: int) -> Optional[int]:
    """
    Common modulus attack
    
    Given: same plaintext m encrypted with (n, e1) and (n, e2)
           where gcd(e1, e2) = 1
    
    Recover: m
    
    Method: Find a, b such that a*e1 + b*e2 = 1
            Then m = c1^a * c2^b mod n
    """
    # Extended Euclidean algorithm
    gcd_val, a, b = extended_gcd(e1, e2)
    
    if gcd_val != 1:
        return None  # Attack doesn't work if e1, e2 not coprime
    
    # Compute m = c1^a * c2^b mod n
    # Handle negative exponents
    if a < 0:
        c1 = pow(c1, -1, n)
        a = -a
    if b < 0:
        c2 = pow(c2, -1, n)
        b = -b
    
    m = (pow(c1, a, n) * pow(c2, b, n)) % n
    
    return m


# ============================================================================
# BROADCAST ATTACK
# ============================================================================

def chinese_remainder_theorem(residues: List[int], moduli: List[int]) -> int:
    """
    Solve system of congruences using CRT
    
    x == a_i (mod n_i) for all i
    """
    if len(residues) != len(moduli):
        raise ValueError("Residues and moduli must have same length")
    
    # Compute N = product of all moduli
    N = 1
    for n in moduli:
        N *= n
    
    result = 0
    for a_i, n_i in zip(residues, moduli):
        N_i = N // n_i
        # Find M_i such that N_i * M_i == 1 (mod n_i)
        _, M_i, _ = extended_gcd(N_i, n_i)
        M_i = M_i % n_i
        result += a_i * N_i * M_i
    
    return result % N


def broadcast_attack(ciphertexts: List[int], moduli: List[int], e: int) -> Optional[int]:
    """
    Broadcast attack on RSA with small e
    
    Given: same message m sent to k recipients
           with public keys (n_i, e) where e is small (e.g., 3)
    
    Recover: m
    
    Condition: Need at least e ciphertexts
    Method: Use CRT to find m^e mod (n1*n2*...), then take e-th root
    """
    if len(ciphertexts) < e:
        return None  # Need at least e ciphertexts
    
    # Use first e ciphertexts
    c_list = ciphertexts[:e]
    n_list = moduli[:e]
    
    # Apply CRT to get m^e mod (n1*n2*...*ne)
    m_e = chinese_remainder_theorem(c_list, n_list)
    
    # Take e-th root (works because m^e < n1*n2*...*ne for typical parameters)
    m = int(m_e ** (1.0 / e) + 0.5)
    
    # Verify
    if pow(m, e, n_list[0]) == c_list[0]:
        return m
    
    # Try nearby values
    for delta in range(-10, 10):
        m_candidate = m + delta
        if m_candidate > 0 and pow(m_candidate, e, n_list[0]) == c_list[0]:
            return m_candidate
    
    return None


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """Main entry point for RSA Attacks Lab"""
    
    # Validate
    errors = validate_parameters(params, PARAMETERS)
    if errors:
        raise ValueError(f"Invalid parameters: {', '.join(errors)}")
    
    mode = params['mode']
    bits = params.get('bits', 512)
    exp_id = create_experiment_id()
    
    if mode == 'wiener_attack':
        print("Generating vulnerable RSA key (small d)...")
        
        # Generate key with conditions that make d small
        # Use large e to force small d
        from Algorithms.utilities import generate_prime
        
        p = generate_prime(bits // 2)
        q = generate_prime(bits // 2)
        n = p * q
        phi = (p - 1) * (q - 1)
        
        # Choose e close to phi to get small d
        e = phi - 12345  # Arbitrary offset
        while gcd(e, phi) != 1:
            e -= 1
        
        d = pow(e, -1, phi)
        
        print(f"Generated key: n={n.bit_length()} bits, d={d.bit_length()} bits")
        
        # Check Wiener threshold
        wiener_threshold = n ** 0.25 / 3
        vulnerable = d < wiener_threshold
        
        print(f"Wiener threshold: {wiener_threshold:.0f}")
        print(f"Vulnerable: {vulnerable}")
        
        # Attempt attack
        if vulnerable:
            print("Attempting Wiener's attack...")
            recovered_d, attack_time = benchmark(wiener_attack, n, e)
            
            results = {
                'n': n,
                'e': e,
                'true_d': d,
                'recovered_d': recovered_d,
                'success': recovered_d == d,
                'attack_time_ms': attack_time,
                'conditions': {
                    'd_bits': d.bit_length(),
                    'n_bits': n.bit_length(),
                    'wiener_threshold': wiener_threshold,
                    'vulnerable': vulnerable
                },
                'mitigation': [
                    'Use d > n^(1/4) / 3',
                    'Use standard e=65537',
                    'Ensure d is sufficiently large'
                ]
            }
        else:
            results = {
                'n': n,
                'e': e,
                'true_d': d,
                'success': False,
                'message': 'Key not vulnerable to Wiener attack',
                'conditions': {
                    'd_bits': d.bit_length(),
                    'n_bits': n.bit_length(),
                    'wiener_threshold': wiener_threshold,
                    'vulnerable': vulnerable
                }
            }
    
    elif mode == 'common_modulus':
        print("Demonstrating common modulus attack...")
        
        # Generate single key pair
        pub, priv = keygen(bits, 65537)
        n = pub.n
        
        # Use two different public exponents
        e1 = 65537
        e2 = 3
        
        # Generate random message
        import random
        m = random.randint(2, n // 100)
        
        print(f"Message: {m}")
        print(f"Encrypting with e1={e1} and e2={e2}...")
        
        # Encrypt with both exponents
        c1 = pow(m, e1, n)
        c2 = pow(m, e2, n)
        
        # Attack
        print("Attempting common modulus attack...")
        recovered_m, attack_time = benchmark(common_modulus_attack, n, e1, e2, c1, c2)
        
        results = {
            'n': n,
            'e1': e1,
            'e2': e2,
            'original_message': m,
            'ciphertext1': c1,
            'ciphertext2': c2,
            'recovered_message': recovered_m,
            'success': recovered_m == m,
            'attack_time_ms': attack_time,
            'conditions': {
                'same_modulus': True,
                'gcd_e1_e2': gcd(e1, e2),
                'coprime_exponents': gcd(e1, e2) == 1
            },
            'mitigation': [
                'Never reuse same modulus n with different exponents',
                'Use separate key pairs for each use case',
                'Implement key rotation policies'
            ]
        }
    
    elif mode == 'broadcast_attack':
        e = params.get('e', 3)
        print(f"Demonstrating broadcast attack with e={e}...")
        
        # Generate e different recipients
        recipients = []
        for i in range(e):
            pub, priv = keygen(bits, e)
            recipients.append({'pub': pub, 'priv': priv})
        
        # Generate message (must be small enough)
        import random
        m = random.randint(2, 10**20)
        
        print(f"Sending message {m} to {e} recipients...")
        
        # Encrypt for each recipient
        ciphertexts = []
        moduli = []
        for recipient in recipients:
            rsa = RSA(recipient['pub'], recipient['priv'])
            c = rsa.encrypt_int(m)
            ciphertexts.append(c)
            moduli.append(recipient['pub'].n)
        
        # Attack
        print("Attempting broadcast attack...")
        recovered_m, attack_time = benchmark(broadcast_attack, ciphertexts, moduli, e)
        
        results = {
            'e': e,
            'num_recipients': len(recipients),
            'original_message': m,
            'ciphertexts': ciphertexts,
            'moduli_bits': [n.bit_length() for n in moduli],
            'recovered_message': recovered_m,
            'success': recovered_m == m,
            'attack_time_ms': attack_time,
            'conditions': {
                'small_e': e <= 5,
                'same_message': True,
                'sufficient_ciphertexts': len(ciphertexts) >= e
            },
            'mitigation': [
                'Use larger e (e.g., 65537)',
                'Add random padding to each message (OAEP)',
                'Never send identical messages to multiple recipients'
            ]
        }
    
    elif mode == 'attack_analysis':
        # Analyze multiple attack scenarios
        print("Running comprehensive attack analysis...")
        
        analysis = []
        
        # Test 1: Wiener vulnerability with different d sizes
        for d_ratio in [0.1, 0.25, 0.3, 0.35]:
            from Algorithms.utilities import generate_prime
            p = generate_prime(bits // 2)
            q = generate_prime(bits // 2)
            n = p * q
            phi = (p - 1) * (q - 1)
            
            # Target d size
            target_d = int(n ** d_ratio)
            e = pow(target_d, -1, phi)
            d = pow(e, -1, phi)
            
            wiener_threshold = n ** 0.25 / 3
            vulnerable = d < wiener_threshold
            
            analysis.append({
                'attack': 'Wiener',
                'd_ratio': d_ratio,
                'd_bits': d.bit_length(),
                'threshold': wiener_threshold,
                'vulnerable': vulnerable,
                'estimated_complexity': 'polynomial' if vulnerable else 'exponential'
            })
        
        # Test 2: Common modulus scenarios
        analysis.append({
            'attack': 'Common Modulus',
            'vulnerable': True,
            'condition': 'Same n, different coprime e',
            'estimated_complexity': 'polynomial (extended GCD)',
            'real_world_likelihood': 'Low (poor practice)'
        })
        
        # Test 3: Broadcast attack scenarios
        for e in [3, 5, 17]:
            analysis.append({
                'attack': 'Broadcast',
                'e': e,
                'vulnerable': e <= 5,
                'required_ciphertexts': e,
                'estimated_complexity': 'polynomial (CRT + root finding)',
                'real_world_likelihood': 'Medium for e=3, Low for larger e'
            })
        
        results = {
            'analysis': analysis,
            'summary': {
                'total_scenarios': len(analysis),
                'vulnerable_count': sum(1 for a in analysis if a.get('vulnerable', False)),
                'recommendations': [
                    'Use e=65537 (F4)',
                    'Ensure d > n^(1/4) / 3',
                    'Never reuse modulus with different exponents',
                    'Use proper padding (OAEP/PSS)',
                    'Implement key rotation'
                ]
            }
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
    print("Testing RSA Attacks Lab\n")
    
    # Test 1: Wiener attack
    print("Test 1: Wiener's attack on small d")
    result1 = run({'mode': 'wiener_attack', 'bits': 512})
    print(f"  Success: {result1['results']['success']}")
    print(f"  Vulnerable: {result1['results']['conditions']['vulnerable']}\n")
    
    # Test 2: Common modulus
    print("Test 2: Common modulus attack")
    result2 = run({'mode': 'common_modulus', 'bits': 512})
    print(f"  Success: {result2['results']['success']}")
    print(f"  Time: {result2['results']['attack_time_ms']:.4f} ms\n")
    
    # Test 3: Broadcast attack
    print("Test 3: Broadcast attack with e=3")
    result3 = run({'mode': 'broadcast_attack', 'bits': 256, 'e': 3})
    print(f"  Success: {result3['results']['success']}")
    print(f"  Time: {result3['results']['attack_time_ms']:.4f} ms\n")
    
    print("[OK] All tests completed!")
