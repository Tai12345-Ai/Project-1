"""
⚡ Exponentiation & Order Lab

Interactive research lab for modular exponentiation algorithms (CLRS 31.6)

Features:
- Multiple exponentiation algorithms (naive, square-and-multiply, Montgomery)
- Operation counting and complexity analysis
- Binary representation visualization
- Order computation for elements in Z*_n
- Primitive root finding

CLRS Sections:
- 31.6: Powers of an element
"""

from typing import Dict, Any, List, Tuple, Optional
import sys
import os
import time

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
from Algorithms.utilities import gcd

# ============================================================================
# LAB METADATA
# ============================================================================

NAME = "Exponentiation & Order Lab"
DESCRIPTION = "Modular exponentiation algorithms, order computation, primitive roots"
LONG_DESCRIPTION = """
This lab explores modular exponentiation - the core operation in RSA encryption
and decryption - from CLRS Section 31.6.

Algorithms implemented:
1. Naive exponentiation - O(b) multiplications
2. Square-and-Multiply (binary method) - O(log b) multiplications
3. Binary representation visualization

Additional features:
- Operation counting for complexity analysis
- Order computation: smallest k where a^k ≡ 1 (mod n)
- Primitive root detection
- Performance benchmarking

Perfect for understanding why RSA encryption/decryption is efficient!
"""

PHASE = 1
CLRS_SECTIONS = ["31.6"]
STATUS = "production"

# ============================================================================
# PARAMETER SCHEMA
# ============================================================================

PARAMETERS = {
    'mode': {
        'type': str,
        'required': True,
        'choices': ['compare_algorithms', 'visualize_binary', 'compute_order', 'find_primitive_root'],
        'description': 'Operation mode'
    },
    'a': {
        'type': int,
        'required': False,
        'description': 'Base (for exponentiation)'
    },
    'b': {
        'type': int,
        'required': False,
        'min': 0,
        'description': 'Exponent'
    },
    'n': {
        'type': int,
        'required': False,
        'min': 2,
        'description': 'Modulus'
    }
}

OUTPUT_FORMAT = {
    'result': {'type': 'number', 'description': 'Computation result'},
    'operations': {'type': 'object', 'description': 'Operation counts'},
    'comparison': {'type': 'object', 'description': 'Algorithm comparison'},
    'visualization': {'type': 'object', 'description': 'Binary representation'}
}

EXAMPLES = [
    {
        'name': 'Compare Exponentiation Algorithms',
        'description': 'Compare naive vs square-and-multiply',
        'parameters': {'mode': 'compare_algorithms', 'a': 7, 'b': 560, 'n': 561}
    },
    {
        'name': 'Visualize Binary Method',
        'description': 'Show square-and-multiply steps',
        'parameters': {'mode': 'visualize_binary', 'a': 3, 'b': 13, 'n': 17}
    },
    {
        'name': 'Compute Order',
        'description': 'Find order of element in Z*_n',
        'parameters': {'mode': 'compute_order', 'a': 3, 'n': 7}
    }
]

# ============================================================================
# EXPONENTIATION ALGORITHMS
# ============================================================================

def naive_modexp(a: int, b: int, n: int) -> Tuple[int, Dict[str, int]]:
    """
    Naive modular exponentiation: compute a^b mod n
    Uses b-1 multiplications
    
    Returns: (result, operations_count)
    """
    ops = {'multiplications': 0, 'modulo': 0}
    
    result = 1
    for _ in range(b):
        result = result * a
        ops['multiplications'] += 1
        result = result % n
        ops['modulo'] += 1
    
    return result, ops


def square_and_multiply(a: int, b: int, n: int) -> Tuple[int, Dict[str, int]]:
    """
    Square-and-multiply (binary method): compute a^b mod n
    Uses O(log b) multiplications
    
    Returns: (result, operations_count)
    """
    ops = {'multiplications': 0, 'modulo': 0, 'squares': 0, 'multiplies': 0}
    
    result = 1
    base = a % n
    ops['modulo'] += 1
    
    while b > 0:
        if b % 2 == 1:
            result = (result * base) % n
            ops['multiplications'] += 1
            ops['multiplies'] += 1
            ops['modulo'] += 1
        
        base = (base * base) % n
        ops['multiplications'] += 1
        ops['squares'] += 1
        ops['modulo'] += 1
        
        b = b // 2
    
    return result, ops


def square_and_multiply_detailed(a: int, b: int, n: int) -> Tuple[int, List[Dict]]:
    """
    Square-and-multiply with detailed step tracking
    
    Returns: (result, steps)
    """
    steps = []
    
    # Binary representation
    binary = bin(b)[2:]  # Remove '0b' prefix
    steps.append({
        'operation': 'Binary representation',
        'binary': binary,
        'description': f'{b} in binary = {binary}'
    })
    
    result = 1
    base = a % n
    
    steps.append({
        'operation': 'Initialize',
        'result': result,
        'base': base,
        'description': f'result = 1, base = {a} mod {n} = {base}'
    })
    
    for i, bit in enumerate(reversed(binary)):
        step_info = {'bit_position': i, 'bit_value': bit}
        
        if bit == '1':
            old_result = result
            result = (result * base) % n
            step_info['operation'] = 'Multiply'
            step_info['calculation'] = f'{old_result} * {base} mod {n} = {result}'
            step_info['result'] = result
        
        if i < len(binary) - 1:  # Don't square on last iteration
            old_base = base
            base = (base * base) % n
            step_info['square'] = f'{old_base}^2 mod {n} = {base}'
            step_info['base'] = base
        
        steps.append(step_info)
    
    return result, steps


# ============================================================================
# ORDER COMPUTATION
# ============================================================================

def compute_order(a: int, n: int, max_order: int = 10000) -> Optional[int]:
    """
    Compute order of a in Z*_n
    
    Order is the smallest positive integer k such that a^k ≡ 1 (mod n)
    
    Returns: order or None if not found within max_order
    """
    if gcd(a, n) != 1:
        return None  # a must be coprime to n
    
    current = a % n
    for k in range(1, min(max_order, n) + 1):
        if current == 1:
            return k
        current = (current * a) % n
    
    return None


def euler_phi(n: int) -> int:
    """
    Compute Euler's totient function phi(n)
    Number of integers in [1, n] coprime to n
    """
    result = n
    p = 2
    
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    
    if n > 1:
        result -= result // n
    
    return result


def is_primitive_root(a: int, n: int, phi_n: Optional[int] = None) -> bool:
    """
    Check if a is a primitive root modulo n
    
    A primitive root is an element whose order equals phi(n)
    """
    if phi_n is None:
        phi_n = euler_phi(n)
    
    order = compute_order(a, n, phi_n + 1)
    return order == phi_n


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """Main entry point for Exponentiation & Order Lab"""
    
    # Validate
    errors = validate_parameters(params, PARAMETERS)
    if errors:
        raise ValueError(f"Invalid parameters: {', '.join(errors)}")
    
    mode = params['mode']
    exp_id = create_experiment_id()
    
    if mode == 'compare_algorithms':
        if not all(k in params for k in ['a', 'b', 'n']):
            raise ValueError("compare_algorithms requires 'a', 'b', 'n' parameters")
        
        a = params['a']
        b = params['b']
        n = params['n']
        
        print(f"Computing {a}^{b} mod {n}...")
        
        comparison = {}
        
        # Naive method (only for small b to avoid timeout)
        if b <= 10000:
            result_naive, time_naive = benchmark(naive_modexp, a, b, n)
            comparison['naive'] = {
                'result': result_naive[0],
                'operations': result_naive[1],
                'time_ms': time_naive,
                'complexity': f'O({b})'
            }
        else:
            comparison['naive'] = {
                'result': None,
                'operations': None,
                'time_ms': None,
                'complexity': f'O({b})',
                'note': 'Skipped (exponent too large)'
            }
        
        # Square-and-multiply
        result_sam, time_sam = benchmark(square_and_multiply, a, b, n)
        comparison['square_and_multiply'] = {
            'result': result_sam[0],
            'operations': result_sam[1],
            'time_ms': time_sam,
            'complexity': f'O(log {b}) = O({b.bit_length()})'
        }
        
        # Built-in pow (for reference)
        result_builtin, time_builtin = benchmark(pow, a, b, n)
        comparison['python_builtin'] = {
            'result': result_builtin,
            'time_ms': time_builtin,
            'note': 'Optimized C implementation'
        }
        
        results = {
            'a': a,
            'b': b,
            'n': n,
            'b_bits': b.bit_length(),
            'result': result_sam[0],
            'comparison': comparison,
            'speedup': time_naive / time_sam if b <= 10000 and time_sam > 0 else None
        }
    
    elif mode == 'visualize_binary':
        if not all(k in params for k in ['a', 'b', 'n']):
            raise ValueError("visualize_binary requires 'a', 'b', 'n' parameters")
        
        a = params['a']
        b = params['b']
        n = params['n']
        
        print(f"Visualizing {a}^{b} mod {n} using square-and-multiply...")
        
        result, steps = square_and_multiply_detailed(a, b, n)
        
        results = {
            'a': a,
            'b': b,
            'n': n,
            'result': result,
            'binary_length': b.bit_length(),
            'steps': steps,
            'total_steps': len(steps)
        }
    
    elif mode == 'compute_order':
        if not all(k in params for k in ['a', 'n']):
            raise ValueError("compute_order requires 'a', 'n' parameters")
        
        a = params['a']
        n = params['n']
        
        print(f"Computing order of {a} in Z*_{n}...")
        
        # Check coprimality
        g = gcd(a, n)
        if g != 1:
            results = {
                'a': a,
                'n': n,
                'gcd': g,
                'order': None,
                'error': f'gcd({a}, {n}) = {g} != 1 (not coprime)'
            }
        else:
            phi_n = euler_phi(n)
            order, time_taken = benchmark(compute_order, a, n, phi_n + 1)
            
            is_primitive = order == phi_n
            
            # Show powers
            powers = []
            current = a
            for k in range(1, min(order + 1, 20)):
                powers.append({
                    'k': k,
                    'a_to_k': current,
                    'congruent_to_1': current == 1
                })
                if current == 1:
                    break
                current = (current * a) % n
            
            results = {
                'a': a,
                'n': n,
                'phi_n': phi_n,
                'order': order,
                'is_primitive_root': is_primitive,
                'time_ms': time_taken,
                'powers': powers if len(powers) <= 20 else powers[:20] + [{'note': '... truncated'}]
            }
    
    elif mode == 'find_primitive_root':
        if 'n' not in params:
            raise ValueError("find_primitive_root requires 'n' parameter")
        
        n = params['n']
        
        print(f"Finding primitive roots modulo {n}...")
        
        phi_n = euler_phi(n)
        primitive_roots = []
        
        # Search for primitive roots
        for a in range(2, min(n, 100)):
            if gcd(a, n) == 1:
                if is_primitive_root(a, n, phi_n):
                    primitive_roots.append(a)
                    if len(primitive_roots) >= 10:  # Limit to first 10
                        break
        
        results = {
            'n': n,
            'phi_n': phi_n,
            'primitive_roots': primitive_roots,
            'count': len(primitive_roots),
            'search_range': min(n, 100),
            'note': 'Primitive roots have order phi(n)' if primitive_roots else 'No primitive roots found in range'
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
    print("Testing Exponentiation & Order Lab\n")
    
    # Test 1: Compare algorithms
    print("Test 1: Compare exponentiation algorithms")
    result1 = run({'mode': 'compare_algorithms', 'a': 7, 'b': 560, 'n': 561})
    print(f"  Result: {result1['results']['result']}")
    if result1['results']['speedup']:
        print(f"  Speedup: {result1['results']['speedup']:.2f}x\n")
    else:
        print()
    
    # Test 2: Visualize binary method
    print("Test 2: Visualize square-and-multiply")
    result2 = run({'mode': 'visualize_binary', 'a': 3, 'b': 13, 'n': 17})
    print(f"  Result: {result2['results']['result']}")
    print(f"  Total steps: {result2['results']['total_steps']}\n")
    
    # Test 3: Compute order
    print("Test 3: Compute order of 3 in Z*_7")
    result3 = run({'mode': 'compute_order', 'a': 3, 'n': 7})
    print(f"  Order: {result3['results']['order']}")
    print(f"  Is primitive root: {result3['results']['is_primitive_root']}\n")
    
    # Test 4: Find primitive roots
    print("Test 4: Find primitive roots modulo 11")
    result4 = run({'mode': 'find_primitive_root', 'n': 11})
    print(f"  Primitive roots: {result4['results']['primitive_roots']}\n")
    
    print("[OK] All tests completed!")
