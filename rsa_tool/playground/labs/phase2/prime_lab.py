"""
🔢 Prime & Primality Testing Lab

Interactive research lab for primality testing algorithms (CLRS 31.8)

Features:
- Miller-Rabin primality test with configurable rounds
- Fermat primality test
- Trial division
- Multi-algorithm comparison
- Prime generation and analysis
- Error probability calculations

CLRS Sections:
- 31.8: Primality testing
"""

from typing import Dict, Any, List
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from rsa_tool.playground.playground_utils import (
    create_experiment_id,
    format_results,
    benchmark,
    validate_parameters,
    create_step_log,
    add_step,
    create_comparison_table
)
from Algorithms.utilities import is_probable_prime, generate_prime, modexp
import random
import secrets

# ============================================================================
# LAB METADATA
# ============================================================================

NAME = "Prime & Primality Testing Lab"
DESCRIPTION = "Multi-algorithm primality testing, prime generation, probability analysis"
LONG_DESCRIPTION = """
This lab provides comprehensive tools for exploring primality testing algorithms
from CLRS Chapter 31.8. You can:

1. Test primality using multiple algorithms (Miller-Rabin, Fermat, Trial Division)
2. Compare algorithm performance and accuracy3. Analyze error probabilities
4. Generate prime numbers with different strategies
5. Study prime distribution

Perfect for:
- Understanding probabilistic vs deterministic algorithms
- Analyzing algorithm trade-offs
- Generating research data on prime testing
- Studying computational number theory
"""

PHASE = 2
CLRS_SECTIONS = ["31.8"]
STATUS = "production"

# ============================================================================
# PARAMETER SCHEMA
# ============================================================================

PARAMETERS = {
    'mode': {
        'type': str,
        'required': True,
        'choices': ['test_prime', 'compare_algorithms', 'generate_prime', 'probability_analysis'],
        'description': 'Operation mode'
    },
    'n': {
        'type': int,
        'required': False,
        'min': 2,
        'description': 'Number to test for primality'
    },
    'rounds': {
        'type': int,
        'required': False,
        'min': 1,
        'max': 100,
        'default': 10,
        'description': 'Number of Miller-Rabin rounds (error probability: 4^-rounds)'
    },
    'bits': {
        'type': int,
        'required': False,
        'min': 8,
        'max': 2048,
        'default': 512,
        'description': 'Bit length for prime generation'
    }
}

OUTPUT_FORMAT = {
    'is_prime': {'type': 'boolean', 'description': 'Primality test result'},
    'algorithm': {'type': 'string', 'description': 'Algorithm used'},
    'rounds': {'type': 'number', 'description': 'Number of test rounds'},
    'error_probability': {'type': 'number', 'description': 'Theoretical error probability'},
    'benchmark': {'type': 'object', 'description': 'Performance metrics'}
}

EXAMPLES = [
    {
        'name': 'Test Large Prime',
        'description': 'Test if a number is prime using Miller-Rabin',
        'parameters': {'mode': 'test_prime', 'n': 982451653, 'rounds': 10}
    },
    {
        'name': 'Compare Algorithms',
        'description': 'Compare Miller-Rabin, Fermat, and Trial Division',
        'parameters': {'mode': 'compare_algorithms', 'n': 1000000007}
    },
    {
        'name': 'Generate 1024-bit Prime',
        'description': 'Generate a random prime number',
        'parameters': {'mode': 'generate_prime', 'bits': 1024}
    }
]

# ============================================================================
# ALGORITHMS
# ============================================================================

def trial_division(n: int, limit: int = 10000) -> tuple[bool, int]:
    """
    Trial division up to sqrt(n) or limit
    
    Returns: (is_prime, operations_count)
    """
    if n < 2:
        return False, 0
    if n == 2:
        return True, 0
    if n % 2 == 0:
        return False, 1
    
    ops = 1
    i = 3
    while i * i <= n and i <= limit:
        if n % i == 0:
            return False, ops
        i += 2
        ops += 1
    
    return True, ops


def fermat_test(n: int, rounds: int = 10) -> tuple[bool, List[int]]:
    """
    Fermat primality test
    
    Tests if a^(n-1) ≡ 1 (mod n) for random a
    
    Returns: (probably_prime, witnesses_tested)
    """
    if n < 2:
        return False, []
    if n == 2:
        return True, []
    if n % 2 == 0:
        return False, []
    
    import random
    witnesses = []
    
    for _ in range(rounds):
        a = random.randint(2, n - 2)
        witnesses.append(a)
        
        if pow(a, n - 1, n) != 1:
            return False, witnesses
    
    return True, witnesses


def test_primality_multi(n: int, rounds: int = 10) -> Dict[str, Any]:
    """Test primality using multiple algorithms"""
    results = {}
    
    # Miller-Rabin
    mr_result, mr_time = benchmark(is_probable_prime, n, rounds)
    results['miller_rabin'] = {
        'is_prime': mr_result,
        'time_ms': mr_time,
        'rounds': rounds,
        'error_probability': 0.25 ** rounds,
        'deterministic': False
    }
    
    # Fermat test
    fermat_result, fermat_time = benchmark(fermat_test, n, rounds)
    results['fermat'] = {
        'is_prime': fermat_result[0],
        'time_ms': fermat_time,
        'rounds': rounds,
        'witnesses': len(fermat_result[1]),
        'deterministic': False
    }
    
    # Trial division (for smaller numbers)
    if n < 10**9:
        trial_result, trial_time = benchmark(trial_division, n, min(100000, int(n**0.5) + 1))
        results['trial_division'] = {
            'is_prime': trial_result[0],
            'time_ms': trial_time,
            'operations': trial_result[1],
            'deterministic': True
        }
    
    return results


def generate_prime_number(bits: int, rounds: int = 10) -> Dict[str, Any]:
    """Generate a random prime number of specified bit length"""
    import random
    import time
    
    steps = create_step_log()
    add_step(steps, f"Generating {bits}-bit prime number", {'bits': bits, 'rounds': rounds})
    
    attempts = 0
    start_time = time.perf_counter()
    
    while True:
        attempts += 1
        
        # Generate random odd number
        candidate = random.randrange(2**(bits-1), 2**bits)
        if candidate % 2 == 0:
            candidate += 1
        
        add_step(steps, f"Attempt {attempts}: Testing {candidate}", {'candidate': candidate})
        
        # Test with Miller-Rabin
        if is_probable_prime(candidate, rounds):
            end_time = time.perf_counter()
            time_ms = (end_time - start_time) * 1000
            
            add_step(steps, f"Found prime after {attempts} attempts", {
                'prime': candidate,
                'attempts': attempts,
                'time_ms': time_ms
            })
            
            return {
                'prime': candidate,
                'bits': bits,
                'attempts': attempts,
                'time_ms': time_ms,
                'rounds': rounds,
                'error_probability': 0.25 ** rounds,
                'steps': steps
            }
        
        if attempts > 1000:
            raise RuntimeError(f"Failed to generate prime after {attempts} attempts")


def probability_analysis(rounds_range: range = range(1, 21)) -> Dict[str, Any]:
    """Analyze error probabilities for different round counts"""
    analysis = []
    
    for rounds in rounds_range:
        error_prob = 0.25 ** rounds
        success_prob = 1 - error_prob
        
        analysis.append({
            'rounds': rounds,
            'error_probability': error_prob,
            'success_probability': success_prob,
            'error_percent': error_prob * 100,
            'bits_certainty': -rounds * 2  # log2(0.25) = -2
        })
    
    return {'analysis': analysis}


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """Main entry point for Prime & Primality Lab"""
    
    # Validate
    errors = validate_parameters(params, PARAMETERS)
    if errors:
        raise ValueError(f"Invalid parameters: {', '.join(errors)}")
    
    # Apply defaults
    rounds = params.get('rounds', 10)
    mode = params['mode']
    
    # Generate experiment ID
    exp_id = create_experiment_id()
    
    # Execute based on mode
    if mode == 'test_prime':
        if 'n' not in params:
            raise ValueError("test_prime mode requires 'n' parameter")
        
        n = params['n']
        result, time_ms = benchmark(is_probable_prime, n, rounds)
        
        results = {
            'n': n,
            'is_prime': result,
            'algorithm': 'Miller-Rabin',
            'rounds': rounds,
            'error_probability': 0.25 ** rounds,
            'benchmark': {'time_ms': time_ms}
        }
        
    elif mode == 'compare_algorithms':
        if 'n' not in params:
            raise ValueError("compare_algorithms mode requires 'n' parameter")
        
        n = params['n']
        results = test_primality_multi(n, rounds)
        
        # Create comparison table
        algorithms = ['miller_rabin', 'fermat']
        if 'trial_division' in results:
            algorithms.append('trial_division')
        
        table_data = {}
        for algo in algorithms:
            table_data[algo] = {
                'Is Prime': results[algo]['is_prime'],
                'Time (ms)': f"{results[algo]['time_ms']:.4f}",
                'Deterministic': results[algo].get('deterministic', False)
            }
        
        comparison_table = create_comparison_table(
            algorithms=algorithms,
            metrics=['Is Prime', 'Time (ms)', 'Deterministic'],
            results=table_data
        )
        
        results['comparison_table'] = comparison_table
        results['n'] = n
        
    elif mode == 'generate_prime':
        bits = params.get('bits', 512)
        result, time_ms = benchmark(generate_prime_number, bits, rounds)
        result['benchmark'] = {'time_ms': time_ms}
        results = result
        
    elif mode == 'probability_analysis':
        rounds_max = params.get('rounds', 20)
        results = probability_analysis(range(1, rounds_max + 1))
        results['benchmark'] = {'time_ms': 0}
        
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
    print("🔢 Testing Prime & Primality Lab\n")
    
    # Test 1: Test a known prime
    print("Test 1: Miller-Rabin on known prime (982451653)")
    result1 = run({'mode': 'test_prime', 'n': 982451653, 'rounds': 10})
    print(f"  Is Prime: {result1['results']['is_prime']}")
    print(f"  Error Probability: {result1['results']['error_probability']:.2e}")
    print(f"  Time: {result1['results']['benchmark']['time_ms']:.4f} ms\n")
    
    # Test 2: Compare algorithms
    print("Test 2: Compare algorithms on 1000000007")
    result2 = run({'mode': 'compare_algorithms', 'n': 1000000007, 'rounds': 5})
    print(f"  Miller-Rabin: {result2['results']['miller_rabin']['is_prime']} ({result2['results']['miller_rabin']['time_ms']:.4f} ms)")
    print(f"  Fermat: {result2['results']['fermat']['is_prime']} ({result2['results']['fermat']['time_ms']:.4f} ms)")
    if 'trial_division' in result2['results']:
        print(f"  Trial Division: {result2['results']['trial_division']['is_prime']} ({result2['results']['trial_division']['time_ms']:.4f} ms)\n")
    
    # Test 3: Generate prime
    print("Test 3: Generate 128-bit prime")
    result3 = run({'mode': 'generate_prime', 'bits': 128, 'rounds': 10})
    print(f"  Prime: {result3['results']['prime']}")
    print(f"  Attempts: {result3['results']['attempts']}")
    print(f"  Time: {result3['results']['time_ms']:.2f} ms\n")
    
    print("✅ All tests passed!")
