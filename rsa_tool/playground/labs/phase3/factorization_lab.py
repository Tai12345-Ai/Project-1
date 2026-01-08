"""
🔨 Factorization Lab

Interactive research lab for integer factorization algorithms (CLRS 31.9)

Features:
- Multiple factorization algorithms (Pollard Rho, Fermat, Trial Division)
- Benchmark & comparison across algorithms
- Security analysis for RSA (weak key detection)
- Attack scenario simulation

CLRS Sections:
- 31.9: Integer factorization
"""

from typing import Dict, Any, List, Tuple, Optional
import sys
import os
import random
import time
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
from Algorithms.pollard_rho import pollard_rho
from Algorithms.utilities import gcd

# ============================================================================
# LAB METADATA
# ============================================================================

NAME = "Factorization Lab"
DESCRIPTION = "Integer factorization algorithms, RSA security analysis, attack simulation"
LONG_DESCRIPTION = """
This lab implements multiple integer factorization algorithms from CLRS 31.9
and analyzes their effectiveness against RSA security.

Algorithms implemented:
1. Trial Division - deterministic, slow for large factors
2. Pollard's Rho - probabilistic, effective for medium factors
3. Fermat's Method - efficient when factors are close

Use cases:
- Compare algorithm performance on different inputs
- Analyze RSA weak key vulnerabilities
- Simulate factorization attacks
- Estimate time-to-factor for different key sizes

Perfect for understanding "why RSA is secure" and "when it's not".
"""

PHASE = 3
CLRS_SECTIONS = ["31.9"]
STATUS = "production"

# ============================================================================
# PARAMETER SCHEMA
# ============================================================================

PARAMETERS = {
    'mode': {
        'type': str,
        'required': True,
        'choices': ['factor_single', 'compare_algorithms', 'weak_key_analysis', 'attack_simulation'],
        'description': 'Operation mode'
    },
    'n': {
        'type': int,
        'required': False,
        'description': 'Number to factorize (for factor_single mode)'
    },
    'bits': {
        'type': int,
        'required': False,
        'min': 16,
        'max': 128,
        'default': 64,
        'description': 'Bit size for composite generation'
    },
    'p_q_ratio': {
        'type': float,
        'required': False,
        'min': 1.0,
        'max': 1000.0,
        'default': 1.5,
        'description': 'Ratio between p and q (for weak key testing)'
    }
}

OUTPUT_FORMAT = {
    'factors': {'type': 'array', 'description': 'Prime factors found'},
    'algorithm': {'type': 'string', 'description': 'Algorithm used'},
    'time_ms': {'type': 'number', 'description': 'Execution time'},
    'iterations': {'type': 'number', 'description': 'Algorithm iterations'},
    'success': {'type': 'boolean', 'description': 'Whether factorization succeeded'}
}

EXAMPLES = [
    {
        'name': 'Factor Small Composite',
        'description': 'Factorize using Pollard Rho',
        'parameters': {'mode': 'factor_single', 'n': 1073676287}
    },
    {
        'name': 'Compare Algorithms',
        'description': 'Benchmark all algorithms on 64-bit composite',
        'parameters': {'mode': 'compare_algorithms', 'bits': 64}
    },
    {
        'name': 'Weak Key Analysis',
        'description': 'Test factorization on close primes',
        'parameters': {'mode': 'weak_key_analysis', 'bits': 64, 'p_q_ratio': 1.1}
    }
]

# ============================================================================
# FACTORIZATION ALGORITHMS
# ============================================================================

def trial_division(n: int, limit: Optional[int] = None) -> Tuple[List[int], int]:
    """
    Trial division factorization
    
    Returns: (factors, iterations)
    """
    if limit is None:
        limit = min(int(n**0.5) + 1, 10**6)
    
    factors = []
    iterations = 0
    
    # Factor out 2s
    while n % 2 == 0:
        factors.append(2)
        n //= 2
        iterations += 1
    
    # Try odd divisors
    d = 3
    while d * d <= n and d <= limit:
        while n % d == 0:
            factors.append(d)
            n //= d
            iterations += 1
        d += 2
        iterations += 1
        
        if iterations > limit:
            break
    
    if n > 1:
        factors.append(n)
    
    return factors, iterations


def fermat_factorization(n: int, max_iterations: int = 100000) -> Tuple[Optional[Tuple[int, int]], int]:
    """
    Fermat's factorization method
    Efficient when factors are close: n = p*q where p ~= q
    
    Returns: ((p, q), iterations) or (None, iterations)
    """
    if n % 2 == 0:
        return ((2, n // 2), 1)
    
    a = math.isqrt(n) + 1
    iterations = 0
    
    for _ in range(max_iterations):
        b2 = a * a - n
        iterations += 1
        
        if b2 >= 0:
            b = math.isqrt(b2)
            if b * b == b2:
                p = a - b
                q = a + b
                if p * q == n and p > 1 and q > 1:
                    return ((p, q), iterations)
        
        a += 1
    
    return (None, iterations)


def pollard_rho_wrapper(n: int, max_iterations: int = 100000) -> Tuple[Optional[int], int]:
    """
    Wrapper for Pollard's Rho with iteration counting
    
    Returns: (factor, iterations)
    """
    iterations = 0
    x, y, d = 2, 2, 1
    
    def f(x):
        return (x * x + 1) % n
    
    while d == 1 and iterations < max_iterations:
        x = f(x)
        y = f(f(y))
        d = gcd(abs(x - y), n)
        iterations += 1
    
    if d != 1 and d != n:
        return (d, iterations)
    return (None, iterations)


# ============================================================================
# COMPOSITE GENERATION
# ============================================================================

def generate_composite(bits: int, p_q_ratio: float = 1.5) -> Tuple[int, int, int]:
    """
    Generate composite n = p*q with controlled p/q ratio
    
    Returns: (n, p, q)
    """
    from Algorithms.utilities import generate_prime
    
    # Generate p
    p_bits = bits // 2
    p = generate_prime(p_bits)
    
    # Generate q based on ratio
    if p_q_ratio < 1.5:
        # Close primes (vulnerable to Fermat)
        q_bits = p_bits
        while True:
            q = generate_prime(q_bits)
            actual_ratio = max(p, q) / min(p, q)
            if abs(actual_ratio - p_q_ratio) < 0.2:
                break
    else:
        # Well-separated primes
        q_bits = bits - p_bits
        q = generate_prime(q_bits)
    
    return (p * q, p, q)


# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def analyze_factorization_difficulty(n: int, p: int, q: int) -> Dict[str, Any]:
    """Analyze why a number is easy/hard to factor"""
    
    analysis = {
        'n': n,
        'p': p,
        'q': q,
        'n_bits': n.bit_length(),
        'vulnerabilities': []
    }
    
    # Check p-q distance
    p_q_diff = abs(p - q)
    sqrt_n = int(n ** 0.5)
    p_q_ratio = max(p, q) / min(p, q)
    
    analysis['p_q_distance'] = {
        'diff': p_q_diff,
        'ratio': p_q_ratio,
        'fermat_vulnerable': p_q_diff < sqrt_n / 100
    }
    
    if p_q_diff < sqrt_n / 100:
        analysis['vulnerabilities'].append({
            'type': 'Fermat Factorization',
            'severity': 'HIGH',
            'description': f'p and q very close (ratio={p_q_ratio:.2f})',
            'estimated_time': 'seconds to minutes'
        })
    
    # Check small factors
    analysis['small_factors'] = {
        'p_small': p < 2**20,
        'q_small': q < 2**20
    }
    
    if p < 2**20 or q < 2**20:
        analysis['vulnerabilities'].append({
            'type': 'Trial Division',
            'severity': 'CRITICAL',
            'description': 'At least one factor is small',
            'estimated_time': 'milliseconds'
        })
    
    # Check size balance
    p_bits = p.bit_length()
    q_bits = q.bit_length()
    bit_imbalance = abs(p_bits - q_bits)
    
    analysis['size_balance'] = {
        'p_bits': p_bits,
        'q_bits': q_bits,
        'imbalance': bit_imbalance,
        'balanced': bit_imbalance < 5
    }
    
    # Overall security assessment
    if len(analysis['vulnerabilities']) == 0:
        analysis['security_level'] = 'GOOD'
        analysis['estimated_time_to_factor'] = 'infeasible for current algorithms'
    elif any(v['severity'] == 'CRITICAL' for v in analysis['vulnerabilities']):
        analysis['security_level'] = 'CRITICAL'
        analysis['estimated_time_to_factor'] = 'seconds'
    else:
        analysis['security_level'] = 'WEAK'
        analysis['estimated_time_to_factor'] = 'minutes to hours'
    
    return analysis


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """Main entry point for Factorization Lab"""
    
    # Validate
    errors = validate_parameters(params, PARAMETERS)
    if errors:
        raise ValueError(f"Invalid parameters: {', '.join(errors)}")
    
    mode = params['mode']
    exp_id = create_experiment_id()
    
    if mode == 'factor_single':
        if 'n' not in params:
            raise ValueError("factor_single mode requires 'n' parameter")
        
        n = params['n']
        
        # Try Pollard Rho first
        print(f"Factoring {n} using Pollard's Rho...")
        factor, iterations = pollard_rho_wrapper(n)
        
        if factor:
            # Found one factor, compute the other
            other = n // factor
            factors = sorted([factor, other])
            
            results = {
                'n': n,
                'factors': factors,
                'algorithm': 'Pollard Rho',
                'iterations': iterations,
                'success': True,
                'verification': factors[0] * factors[1] == n
            }
        else:
            results = {
                'n': n,
                'factors': [],
                'algorithm': 'Pollard Rho',
                'iterations': iterations,
                'success': False,
                'message': 'Factorization failed (number may be prime or too large)'
            }
    
    elif mode == 'compare_algorithms':
        bits = params.get('bits', 64)
        p_q_ratio = params.get('p_q_ratio', 1.5)
        
        print(f"Generating {bits}-bit composite with p/q ratio ~= {p_q_ratio}...")
        n, p, q = generate_composite(bits, p_q_ratio)
        
        print(f"Generated n = {n} (p={p}, q={q})")
        
        comparison = {}
        
        # Trial Division
        print("Testing Trial Division...")
        factors_td, time_td = benchmark(trial_division, n, min(10**6, int(n**0.5)))
        comparison['trial_division'] = {
            'factors': factors_td[0],
            'iterations': factors_td[1],
            'time_ms': time_td,
            'success': len(factors_td[0]) > 1 and all(f in [p, q] for f in factors_td[0])
        }
        
        # Fermat
        print("Testing Fermat Factorization...")
        result_fermat, time_fermat = benchmark(fermat_factorization, n, 100000)
        if result_fermat[0]:
            factors_fermat = list(result_fermat[0])
            comparison['fermat'] = {
                'factors': sorted(factors_fermat),
                'iterations': result_fermat[1],
                'time_ms': time_fermat,
                'success': True
            }
        else:
            comparison['fermat'] = {
                'factors': [],
                'iterations': result_fermat[1],
                'time_ms': time_fermat,
                'success': False
            }
        
        # Pollard Rho
        print("Testing Pollard's Rho...")
        result_rho, time_rho = benchmark(pollard_rho_wrapper, n, 100000)
        if result_rho[0]:
            f1 = result_rho[0]
            f2 = n // f1
            comparison['pollard_rho'] = {
                'factors': sorted([f1, f2]),
                'iterations': result_rho[1],
                'time_ms': time_rho,
                'success': True
            }
        else:
            comparison['pollard_rho'] = {
                'factors': [],
                'iterations': result_rho[1],
                'time_ms': time_rho,
                'success': False
            }
        
        # Analysis
        analysis = analyze_factorization_difficulty(n, p, q)
        
        results = {
            'n': n,
            'true_factors': [p, q],
            'bits': bits,
            'comparison': comparison,
            'analysis': analysis
        }
    
    elif mode == 'weak_key_analysis':
        bits = params.get('bits', 64)
        p_q_ratio = params.get('p_q_ratio', 1.1)
        
        print(f"Generating WEAK {bits}-bit key with p/q ratio ~= {p_q_ratio}...")
        n, p, q = generate_composite(bits, p_q_ratio)
        
        # Analyze vulnerability
        analysis = analyze_factorization_difficulty(n, p, q)
        
        # Try fastest applicable algorithm
        if analysis['p_q_distance']['fermat_vulnerable']:
            print("Key vulnerable to Fermat attack - attempting...")
            result, time_taken = benchmark(fermat_factorization, n, 100000)
            method = 'Fermat'
            success = result[0] is not None
            factors = list(result[0]) if success else []
        else:
            print("Attempting Pollard's Rho...")
            result, time_taken = benchmark(pollard_rho_wrapper, n, 100000)
            method = 'Pollard Rho'
            success = result[0] is not None
            factors = [result[0], n // result[0]] if success else []
        
        results = {
            'n': n,
            'true_factors': [p, q],
            'bits': bits,
            'p_q_ratio': p_q_ratio,
            'analysis': analysis,
            'attack': {
                'method': method,
                'success': success,
                'factors_found': sorted(factors) if factors else [],
                'time_ms': time_taken,
                'iterations': result[1]
            }
        }
    
    elif mode == 'attack_simulation':
        # Simulate attacks on different key sizes
        test_cases = [
            {'bits': 32, 'ratio': 1.5, 'label': '32-bit balanced'},
            {'bits': 48, 'ratio': 1.1, 'label': '48-bit close primes'},
            {'bits': 64, 'ratio': 2.0, 'label': '64-bit separated'},
            {'bits': 80, 'ratio': 1.05, 'label': '80-bit very close'},
        ]
        
        simulation_results = []
        
        for case in test_cases:
            print(f"\nTesting: {case['label']}...")
            n, p, q = generate_composite(case['bits'], case['ratio'])
            analysis = analyze_factorization_difficulty(n, p, q)
            
            # Try Pollard Rho
            result, time_taken = benchmark(pollard_rho_wrapper, n, 50000)
            
            simulation_results.append({
                'label': case['label'],
                'bits': case['bits'],
                'n': n,
                'security_level': analysis['security_level'],
                'vulnerabilities': len(analysis['vulnerabilities']),
                'attack_success': result[0] is not None,
                'time_ms': time_taken
            })
        
        results = {
            'simulation': simulation_results,
            'summary': {
                'total_tests': len(test_cases),
                'successful_attacks': sum(1 for r in simulation_results if r['attack_success']),
                'average_time_ms': sum(r['time_ms'] for r in simulation_results) / len(simulation_results)
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
    print("Testing Factorization Lab\n")
    
    # Test 1: Factor known composite
    print("Test 1: Factor 1073676287 (product of two primes)")
    result1 = run({'mode': 'factor_single', 'n': 1073676287})
    if result1['results']['success']:
        print(f"  [OK] Factors: {result1['results']['factors']}")
        print(f"  Iterations: {result1['results']['iterations']}\n")
    else:
        print(f"  [FAIL] Failed\n")
    
    # Test 2: Compare algorithms
    print("Test 2: Compare algorithms on 48-bit composite")
    result2 = run({'mode': 'compare_algorithms', 'bits': 48, 'p_q_ratio': 1.2})
    print(f"  n = {result2['results']['n']}")
    print(f"  True factors: {result2['results']['true_factors']}")
    for algo, data in result2['results']['comparison'].items():
        status = "[OK]" if data['success'] else "[FAIL]"
        print(f"  {status} {algo}: {data['time_ms']:.4f} ms ({data['iterations']} iterations)")
    print(f"  Security: {result2['results']['analysis']['security_level']}\n")
    
    # Test 3: Weak key analysis
    print("Test 3: Weak key with close primes")
    result3 = run({'mode': 'weak_key_analysis', 'bits': 56, 'p_q_ratio': 1.05})
    attack = result3['results']['attack']
    status = "[OK]" if attack['success'] else "[FAIL]"
    print(f"  {status} Attack method: {attack['method']}")
    print(f"  Time: {attack['time_ms']:.4f} ms")
    print(f"  Vulnerabilities: {len(result3['results']['analysis']['vulnerabilities'])}\n")
    
    print("[OK] All tests completed!")
