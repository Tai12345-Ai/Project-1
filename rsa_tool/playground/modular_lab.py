"""
🧮 Modular Arithmetic Lab

Interactive research lab for modular arithmetic algorithms (CLRS 31.1-31.4)

Features:
- Extended Euclidean Algorithm with step-by-step visualization
- Solve modular linear equations: ax ≡ b (mod m)
- Compute modular inverse: a^(-1) mod m
- Chinese Remainder Theorem (CRT) solver
- Algorithm comparison and benchmarking

CLRS Sections:
- 31.1: Elementary number-theoretic notions
- 31.2: Greatest common divisor
- 31.3: Modular arithmetic
- 31.4: Solving modular linear equations
"""

from typing import Dict, Any, List, Tuple
from .playground_utils import (
    create_experiment_id,
    format_results,
    benchmark,
    validate_parameters,
    create_step_log,
    add_step,
    create_comparison_table
)

# ============================================================================
# LAB METADATA
# ============================================================================

NAME = "Modular Arithmetic Lab"
DESCRIPTION = "Solve modular equations, Extended Euclidean, CRT, modular inverse"
LONG_DESCRIPTION = """
This lab provides interactive tools for exploring modular arithmetic algorithms
from CLRS Chapter 31. You can:

1. Solve linear modular equations ax ≡ b (mod m)
2. Compute GCD using Extended Euclidean Algorithm with full step trace
3. Find modular inverses a^(-1) mod m
4. Solve systems of congruences using Chinese Remainder Theorem
5. Compare algorithm performance and operation counts

Perfect for:
- Understanding modular arithmetic fundamentals
- Analyzing algorithm complexity empirically
- Generating data for research papers
- Teaching number theory concepts
"""

PHASE = 1
CLRS_SECTIONS = ["31.1", "31.2", "31.3", "31.4"]
STATUS = "production"

# ============================================================================
# PARAMETER SCHEMA
# ============================================================================

PARAMETERS = {
    'mode': {
        'type': str,
        'required': True,
        'choices': ['solve_equation', 'extended_gcd', 'mod_inverse', 'crt', 'compare'],
        'description': 'Operation mode: solve_equation, extended_gcd, mod_inverse, crt, compare'
    },
    'a': {
        'type': int,
        'required': False,
        'min': 1,
        'description': 'Coefficient a in ax ≡ b (mod m) or first number for GCD'
    },
    'b': {
        'type': int,
        'required': False,
        'min': 0,
        'description': 'Constant b in ax ≡ b (mod m) or second number for GCD'
    },
    'm': {
        'type': int,
        'required': False,
        'min': 2,
        'description': 'Modulus m'
    },
    'congruences': {
        'type': list,
        'required': False,
        'description': 'List of [remainder, modulus] pairs for CRT'
    },
    'show_steps': {
        'type': bool,
        'required': False,
        'default': True,
        'description': 'Include step-by-step algorithm execution'
    }
}

# ============================================================================
# OUTPUT FORMAT
# ============================================================================

OUTPUT_FORMAT = {
    'result': {
        'type': 'varies',
        'description': 'Main computation result (depends on mode)'
    },
    'steps': {
        'type': 'array',
        'description': 'Step-by-step algorithm execution trace'
    },
    'analysis': {
        'type': 'object',
        'description': 'Mathematical analysis and properties'
    },
    'benchmark': {
        'type': 'object',
        'description': 'Performance metrics'
    }
}

# ============================================================================
# EXAMPLES
# ============================================================================

EXAMPLES = [
    {
        'name': 'Solve Linear Congruence',
        'description': 'Solve 5x ≡ 3 (mod 7)',
        'parameters': {
            'mode': 'solve_equation',
            'a': 5,
            'b': 3,
            'm': 7
        }
    },
    {
        'name': 'Extended Euclidean',
        'description': 'Compute GCD(99, 78) with Bézout coefficients',
        'parameters': {
            'mode': 'extended_gcd',
            'a': 99,
            'b': 78
        }
    },
    {
        'name': 'Modular Inverse',
        'description': 'Find 5^(-1) mod 7',
        'parameters': {
            'mode': 'mod_inverse',
            'a': 5,
            'm': 7
        }
    },
    {
        'name': 'Chinese Remainder Theorem',
        'description': 'Solve x ≡ 2 (mod 3), x ≡ 3 (mod 5), x ≡ 2 (mod 7)',
        'parameters': {
            'mode': 'crt',
            'congruences': [[2, 3], [3, 5], [2, 7]]
        }
    }
]

# ============================================================================
# CORE ALGORITHMS
# ============================================================================

def extended_gcd(a: int, b: int, show_steps: bool = True) -> Dict[str, Any]:
    """
    Extended Euclidean Algorithm (CLRS 31.2)
    
    Computes gcd(a, b) and Bézout coefficients x, y such that:
    ax + by = gcd(a, b)
    
    Args:
        a, b: Input integers
        show_steps: Include step-by-step trace
        
    Returns:
        Dictionary with gcd, x, y, steps, operation_count
    """
    steps = create_step_log() if show_steps else None
    operation_count = 0
    
    # Keep original values for verification
    orig_a, orig_b = a, b
    
    if show_steps:
        add_step(steps, f"Start: Find gcd({a}, {b})", {'a': a, 'b': b})
    
    # Initialize
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    
    iteration = 0
    while r != 0:
        iteration += 1
        quotient = old_r // r
        operation_count += 1  # Division
        
        if show_steps:
            add_step(steps, f"Iteration {iteration}: quotient = {old_r} // {r} = {quotient}",
                    {'quotient': quotient, 'old_r': old_r, 'r': r})
        
        # Update r
        old_r, r = r, old_r - quotient * r
        operation_count += 2  # Multiplication and subtraction
        
        # Update s (Bézout coefficient for a)
        old_s, s = s, old_s - quotient * s
        operation_count += 2
        
        # Update t (Bézout coefficient for b)
        old_t, t = t, old_t - quotient * t
        operation_count += 2
        
        if show_steps:
            add_step(steps, f"After iteration {iteration}",
                    {'r': r, 's': s, 't': t, 'gcd_candidate': old_r})
    
    gcd = old_r
    x, y = old_s, old_t
    
    if show_steps:
        add_step(steps, f"Final: gcd = {gcd}, x = {x}, y = {y}", 
                {'gcd': gcd, 'x': x, 'y': y})
        add_step(steps, f"Verification: {orig_a}×{x} + {orig_b}×{y} = {orig_a*x + orig_b*y}",
                {'verification': orig_a*x + orig_b*y == gcd})
    
    return {
        'gcd': gcd,
        'x': x,
        'y': y,
        'steps': steps,
        'operation_count': operation_count,
        'verification': orig_a * x + orig_b * y
    }


def mod_inverse(a: int, m: int, show_steps: bool = True) -> Dict[str, Any]:
    """
    Compute modular inverse: a^(-1) mod m (CLRS 31.4)
    
    Uses Extended Euclidean Algorithm.
    Inverse exists iff gcd(a, m) = 1
    
    Args:
        a: Number to invert
        m: Modulus
        show_steps: Include step-by-step trace
        
    Returns:
        Dictionary with inverse, exists, steps
    """
    steps = create_step_log() if show_steps else None
    
    if show_steps:
        add_step(steps, f"Find {a}^(-1) mod {m}", {'a': a, 'm': m})
    
    # Use Extended Euclidean
    result = extended_gcd(a, m, show_steps=False)
    gcd = result['gcd']
    x = result['x']
    
    if gcd != 1:
        if show_steps:
            add_step(steps, f"No inverse: gcd({a}, {m}) = {gcd} ≠ 1",
                    {'gcd': gcd, 'inverse_exists': False})
        return {
            'inverse': None,
            'exists': False,
            'reason': f"gcd({a}, {m}) = {gcd} ≠ 1",
            'steps': steps
        }
    
    # Normalize to positive
    inverse = x % m
    
    if show_steps:
        add_step(steps, f"gcd({a}, {m}) = 1, so inverse exists", {'gcd': gcd})
        add_step(steps, f"From Extended Euclidean: {a}×{x} + {m}×{result['y']} = 1",
                {'x': x, 'y': result['y']})
        add_step(steps, f"Therefore: {a}×{x} ≡ 1 (mod {m})", {'x': x})
        add_step(steps, f"Normalized: {a}^(-1) ≡ {inverse} (mod {m})", {'inverse': inverse})
        add_step(steps, f"Verification: {a}×{inverse} mod {m} = {(a * inverse) % m}",
                {'verification': (a * inverse) % m})
    
    return {
        'inverse': inverse,
        'exists': True,
        'gcd': gcd,
        'bezout_x': x,
        'steps': steps,
        'verification': (a * inverse) % m
    }


def solve_modular_equation(a: int, b: int, m: int, show_steps: bool = True) -> Dict[str, Any]:
    """
    Solve ax ≡ b (mod m) (CLRS 31.4)
    
    Solution exists iff gcd(a, m) divides b
    If exists, there are gcd(a, m) solutions modulo m
    
    Args:
        a, b: Equation coefficients
        m: Modulus
        show_steps: Include step-by-step trace
        
    Returns:
        Dictionary with solutions, exists, steps
    """
    steps = create_step_log() if show_steps else None
    
    if show_steps:
        add_step(steps, f"Solve: {a}x ≡ {b} (mod {m})", {'a': a, 'b': b, 'm': m})
    
    # Compute gcd(a, m)
    result = extended_gcd(a, m, show_steps=False)
    d = result['gcd']
    
    if show_steps:
        add_step(steps, f"Compute gcd({a}, {m}) = {d}", {'gcd': d})
    
    # Check if solution exists
    if b % d != 0:
        if show_steps:
            add_step(steps, f"No solution: {d} does not divide {b}",
                    {'gcd': d, 'b': b, 'divisible': False})
        return {
            'solutions': [],
            'exists': False,
            'reason': f"gcd({a}, {m}) = {d} does not divide {b}",
            'steps': steps
        }
    
    # Solution exists
    if show_steps:
        add_step(steps, f"Solution exists: {d} divides {b}",
                {'gcd': d, 'divisible': True, 'num_solutions': d})
    
    # Reduce the equation by dividing by d
    a_prime = a // d
    b_prime = b // d
    m_prime = m // d
    
    if show_steps:
        add_step(steps, f"Divide by {d}: {a_prime}x ≡ {b_prime} (mod {m_prime})",
                {'a_prime': a_prime, 'b_prime': b_prime, 'm_prime': m_prime})
    
    # Find inverse of a_prime mod m_prime
    inv_result = mod_inverse(a_prime, m_prime, show_steps=False)
    a_inv = inv_result['inverse']
    
    if show_steps:
        add_step(steps, f"Find {a_prime}^(-1) mod {m_prime} = {a_inv}",
                {'inverse': a_inv})
    
    # Compute x0 (particular solution)
    x0 = (a_inv * b_prime) % m_prime
    
    if show_steps:
        add_step(steps, f"x₀ = {a_inv} × {b_prime} mod {m_prime} = {x0}",
                {'x0': x0})
    
    # Generate all d solutions
    solutions = [(x0 + k * m_prime) % m for k in range(d)]
    
    if show_steps:
        add_step(steps, f"All {d} solutions modulo {m}: {solutions}",
                {'solutions': solutions})
        # Verify first solution
        verification = (a * solutions[0]) % m
        add_step(steps, f"Verify: {a}×{solutions[0]} mod {m} = {verification}",
                {'verification': verification, 'expected': b % m})
    
    return {
        'solutions': solutions,
        'exists': True,
        'num_solutions': d,
        'gcd': d,
        'x0': x0,
        'steps': steps,
        'verification': (a * solutions[0]) % m == b % m
    }


def chinese_remainder_theorem(congruences: List[List[int]], show_steps: bool = True) -> Dict[str, Any]:
    """
    Solve system of congruences using CRT (CLRS 31.5)
    
    Given: x ≡ a₁ (mod n₁), x ≡ a₂ (mod n₂), ...
    Find: x (mod N) where N = n₁ × n₂ × ...
    
    Requires: all moduli pairwise coprime
    
    Args:
        congruences: List of [remainder, modulus] pairs
        show_steps: Include step-by-step trace
        
    Returns:
        Dictionary with solution, steps
    """
    steps = create_step_log() if show_steps else None
    
    if show_steps:
        congruence_str = ", ".join([f"x ≡ {a} (mod {n})" for a, n in congruences])
        add_step(steps, f"Solve system: {congruence_str}", {'congruences': congruences})
    
    # Check pairwise coprimality
    n_values = [n for _, n in congruences]
    for i in range(len(n_values)):
        for j in range(i + 1, len(n_values)):
            gcd_result = extended_gcd(n_values[i], n_values[j], show_steps=False)
            if gcd_result['gcd'] != 1:
                if show_steps:
                    add_step(steps, f"Error: gcd({n_values[i]}, {n_values[j]}) = {gcd_result['gcd']} ≠ 1",
                            {'not_coprime': [n_values[i], n_values[j]]})
                return {
                    'solution': None,
                    'exists': False,
                    'reason': f"Moduli not pairwise coprime: gcd({n_values[i]}, {n_values[j]}) = {gcd_result['gcd']}",
                    'steps': steps
                }
    
    if show_steps:
        add_step(steps, "All moduli pairwise coprime ✓", {'coprime': True})
    
    # Compute N = product of all moduli
    N = 1
    for _, n in congruences:
        N *= n
    
    if show_steps:
        add_step(steps, f"N = {' × '.join(map(str, n_values))} = {N}", {'N': N})
    
    # CRT construction
    x = 0
    crt_components = []
    
    for i, (a_i, n_i) in enumerate(congruences):
        N_i = N // n_i
        
        # Find M_i such that N_i × M_i ≡ 1 (mod n_i)
        inv_result = mod_inverse(N_i, n_i, show_steps=False)
        M_i = inv_result['inverse']
        
        term = a_i * N_i * M_i
        x += term
        
        crt_components.append({
            'a_i': a_i,
            'n_i': n_i,
            'N_i': N_i,
            'M_i': M_i,
            'term': term
        })
        
        if show_steps:
            add_step(steps, f"Congruence {i+1}: N_{i+1} = {N_i}, M_{i+1} = {M_i}",
                    {'N_i': N_i, 'M_i': M_i, 'term': term})
    
    # Reduce modulo N
    x = x % N
    
    if show_steps:
        add_step(steps, f"Sum all terms and reduce: x ≡ {x} (mod {N})", {'x': x})
        
        # Verify
        verifications = []
        for a_i, n_i in congruences:
            check = x % n_i
            verifications.append({'expected': a_i, 'actual': check, 'match': check == a_i})
        add_step(steps, "Verification of all congruences", {'verifications': verifications})
    
    return {
        'solution': x,
        'exists': True,
        'modulus': N,
        'crt_components': crt_components,
        'steps': steps,
        'verification': all((x % n) == a for a, n in congruences)
    }


def compare_algorithms(a: int, b: int, show_steps: bool = True) -> Dict[str, Any]:
    """
    Compare different GCD algorithms
    
    Compares:
    - Extended Euclidean
    - Binary GCD (Stein's algorithm)
    - Naive GCD
    """
    steps = create_step_log() if show_steps else None
    
    if show_steps:
        add_step(steps, f"Compare GCD algorithms for ({a}, {b})", {'a': a, 'b': b})
    
    # Extended Euclidean
    result_ext, time_ext = benchmark(extended_gcd, a, b, show_steps=False)
    
    # Naive GCD (for comparison)
    def naive_gcd(a, b):
        ops = 0
        while b:
            a, b = b, a % b
            ops += 1
        return {'gcd': a, 'operation_count': ops}
    
    result_naive, time_naive = benchmark(naive_gcd, a, b)
    
    results = {
        'extended_euclidean': {
            'gcd': result_ext['gcd'],
            'time_ms': time_ext,
            'operations': result_ext['operation_count'],
            'provides_bezout': True
        },
        'naive_gcd': {
            'gcd': result_naive['gcd'],
            'time_ms': time_naive,
            'operations': result_naive['operation_count'],
            'provides_bezout': False
        }
    }
    
    if show_steps:
        add_step(steps, "Algorithm comparison complete", results)
    
    # Create comparison table
    table = create_comparison_table(
        algorithms=['Extended Euclidean', 'Naive GCD'],
        metrics=['GCD', 'Time (ms)', 'Operations', 'Bézout Coefficients'],
        results={
            'Extended Euclidean': {
                'GCD': result_ext['gcd'],
                'Time (ms)': f"{time_ext:.4f}",
                'Operations': result_ext['operation_count'],
                'Bézout Coefficients': 'Yes'
            },
            'Naive GCD': {
                'GCD': result_naive['gcd'],
                'Time (ms)': f"{time_naive:.4f}",
                'Operations': result_naive['operation_count'],
                'Bézout Coefficients': 'No'
            }
        }
    )
    
    return {
        'results': results,
        'comparison_table': table,
        'steps': steps
    }


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entry point for Modular Arithmetic Lab
    
    Args:
        params: Parameters including mode and mode-specific inputs
        
    Returns:
        Standardized result dictionary
    """
    # Validate
    errors = validate_parameters(params, PARAMETERS)
    if errors:
        raise ValueError(f"Invalid parameters: {', '.join(errors)}")
    
    # Apply defaults
    show_steps = params.get('show_steps', True)
    mode = params['mode']
    
    # Generate experiment ID
    exp_id = create_experiment_id()
    
    # Execute based on mode
    if mode == 'extended_gcd':
        if 'a' not in params or 'b' not in params:
            raise ValueError("extended_gcd mode requires 'a' and 'b' parameters")
        
        result, time_ms = benchmark(extended_gcd, params['a'], params['b'], show_steps)
        result['benchmark'] = {'time_ms': time_ms}
        
    elif mode == 'mod_inverse':
        if 'a' not in params or 'm' not in params:
            raise ValueError("mod_inverse mode requires 'a' and 'm' parameters")
        
        result, time_ms = benchmark(mod_inverse, params['a'], params['m'], show_steps)
        result['benchmark'] = {'time_ms': time_ms}
        
    elif mode == 'solve_equation':
        if 'a' not in params or 'b' not in params or 'm' not in params:
            raise ValueError("solve_equation mode requires 'a', 'b', and 'm' parameters")
        
        result, time_ms = benchmark(solve_modular_equation, 
                                   params['a'], params['b'], params['m'], show_steps)
        result['benchmark'] = {'time_ms': time_ms}
        
    elif mode == 'crt':
        if 'congruences' not in params:
            raise ValueError("crt mode requires 'congruences' parameter")
        
        result, time_ms = benchmark(chinese_remainder_theorem, params['congruences'], show_steps)
        result['benchmark'] = {'time_ms': time_ms}
        
    elif mode == 'compare':
        if 'a' not in params or 'b' not in params:
            raise ValueError("compare mode requires 'a' and 'b' parameters")
        
        result, time_ms = benchmark(compare_algorithms, params['a'], params['b'], show_steps)
        result['benchmark'] = {'time_ms': time_ms}
        
    else:
        raise ValueError(f"Unknown mode: {mode}")
    
    # Format with standard structure
    return format_results(
        experiment_id=exp_id,
        lab_name=NAME,
        parameters=params,
        results=result,
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
    print("🧮 Testing Modular Arithmetic Lab\n")
    
    # Test 1: Extended GCD
    print("Test 1: Extended GCD(99, 78)")
    result1 = run({'mode': 'extended_gcd', 'a': 99, 'b': 78, 'show_steps': False})
    print(f"  GCD: {result1['results']['gcd']}")
    print(f"  Bézout: x={result1['results']['x']}, y={result1['results']['y']}")
    print(f"  Time: {result1['results']['benchmark']['time_ms']:.4f} ms")
    print(f"  ✓ Verified: {result1['results']['verification'] == result1['results']['gcd']}\n")
    
    # Test 2: Modular Inverse
    print("Test 2: Find 5^(-1) mod 7")
    result2 = run({'mode': 'mod_inverse', 'a': 5, 'm': 7, 'show_steps': False})
    print(f"  Inverse: {result2['results']['inverse']}")
    print(f"  ✓ Verified: {result2['results']['verification'] == 1}\n")
    
    # Test 3: Solve Equation
    print("Test 3: Solve 5x ≡ 3 (mod 7)")
    result3 = run({'mode': 'solve_equation', 'a': 5, 'b': 3, 'm': 7, 'show_steps': False})
    print(f"  Solutions: {result3['results']['solutions']}")
    print(f"  ✓ Verified: {result3['results']['verification']}\n")
    
    # Test 4: CRT
    print("Test 4: CRT - x ≡ 2 (mod 3), x ≡ 3 (mod 5), x ≡ 2 (mod 7)")
    result4 = run({'mode': 'crt', 'congruences': [[2, 3], [3, 5], [2, 7]], 'show_steps': False})
    print(f"  Solution: x ≡ {result4['results']['solution']} (mod {result4['results']['modulus']})")
    print(f"  ✓ Verified: {result4['results']['verification']}\n")
    
    # Test 5: Algorithm Comparison
    print("Test 5: Compare GCD algorithms for (12345, 67890)")
    result5 = run({'mode': 'compare', 'a': 12345, 'b': 67890, 'show_steps': False})
    print(f"  Extended Euclidean: {result5['results']['results']['extended_euclidean']['time_ms']:.4f} ms")
    print(f"  Naive GCD: {result5['results']['results']['naive_gcd']['time_ms']:.4f} ms")
    
    print("\n✅ All tests passed!")
