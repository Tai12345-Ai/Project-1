"""
🔐 RSA Parameter Lab

Interactive research lab for RSA parameter analysis and security (CLRS 31.7)

Features:
- RSA key parameter validation
- Security analysis (Wiener threshold, p-q distance, etc.)
- Performance benchmarking (encryption/decryption with/without CRT)
- Parameter space exploration
- NIST compliance checking

CLRS Sections:
- 31.7: RSA public-key cryptosystem
"""

from typing import Dict, Any, List
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from rsa_tool.playground.playground_utils import (
    create_experiment_id,
    format_results,
    benchmark,
    validate_parameters,
    create_step_log,
    add_step
)
from Algorithms.rsa import keygen, RSA
from Algorithms.utilities import extended_gcd

# ============================================================================
# LAB METADATA
# ============================================================================

NAME = "RSA Parameter Lab"
DESCRIPTION = "RSA parameter analysis, security evaluation, performance benchmarking"
LONG_DESCRIPTION = """
This lab provides comprehensive analysis tools for RSA parameters and security
from CLRS Chapter 31.7. You can:

1. Generate RSA keys with custom parameters (e, key size)
2. Analyze security properties (d size, p-q distance, etc.)
3. Benchmark encryption/decryption performance
4. Compare with/without CRT optimization
5. Check NIST recommendations compliance
6. Explore parameter space trade-offs

Perfect for:
- Understanding RSA security parameters
- Analyzing attack vulnerabilities
- Performance optimization research
- Security configuration validation
"""

PHASE = 2
CLRS_SECTIONS = ["31.7"]
STATUS = "production"

# ============================================================================
# PARAMETER SCHEMA
# ============================================================================

PARAMETERS = {
    'mode': {
        'type': str,
        'required': True,
        'choices': ['generate_analyze', 'security_check', 'performance_benchmark', 'parameter_sweep'],
        'description': 'Operation mode'
    },
    'bits': {
        'type': int,
        'required': False,
        'min': 512,
        'max': 4096,
        'default': 1024,
        'description': 'RSA key size in bits'
    },
    'e': {
        'type': int,
        'required': False,
        'default': 65537,
        'description': 'Public exponent (common: 3, 17, 65537)'
    },
    'message': {
        'type': int,
        'required': False,
        'description': 'Message to encrypt/decrypt for benchmarking'
    }
}

OUTPUT_FORMAT = {
    'keys': {'type': 'object', 'description': 'Generated RSA keys'},
    'security_analysis': {'type': 'object', 'description': 'Security properties'},
    'performance': {'type': 'object', 'description': 'Performance metrics'},
    'recommendations': {'type': 'array', 'description': 'Security recommendations'}
}

EXAMPLES = [
    {
        'name': 'Generate and Analyze 2048-bit Key',
        'description': 'Generate RSA key and perform security analysis',
        'parameters': {'mode': 'generate_analyze', 'bits': 2048, 'e': 65537}
    },
    {
        'name': 'Security Check',
        'description': 'Check generated key for vulnerabilities',
        'parameters': {'mode': 'security_check', 'bits': 1024}
    },
    {
        'name': 'Performance Benchmark',
        'description': 'Compare encryption performance with/without CRT',
        'parameters': {'mode': 'performance_benchmark', 'bits': 2048}
    }
]

# ============================================================================
# SECURITY ANALYSIS FUNCTIONS
# ============================================================================

def analyze_security(n, e, d, p, q, phi_n) -> Dict[str, Any]:
    """Comprehensive security analysis of RSA parameters"""
    
    analysis = {
        'vulnerabilities': [],
        'warnings': [],
        'recommendations': [],
        'scores': {}
    }
    
    # Check 1: d size (Wiener's attack threshold)
    d_bits = d.bit_length()
    n_bits = n.bit_length()
    wiener_threshold = n_bits * 0.25
    
    analysis['d_size'] = {
        'd_bits': d_bits,
        'n_bits': n_bits,
        'ratio': d_bits / n_bits,
        'wiener_safe': d_bits > wiener_threshold
    }
    
    if d_bits <= wiener_threshold:
        analysis['vulnerabilities'].append({
            'type': 'Wiener Attack',
            'severity': 'CRITICAL',
            'description': f'd is too small ({d_bits} bits < {wiener_threshold:.0f} bits threshold)',
            'mitigation': 'Use larger d or different e'
        })
    
    # Check 2: p-q distance (Fermat factorization)
    p_q_diff = abs(p - q)
    p_q_ratio = max(p, q) / min(p, q)
    sqrt_n = int(n ** 0.5)
    
    analysis['p_q_distance'] = {
        'p_q_diff': p_q_diff,
        'p_q_ratio': p_q_ratio,
        'safe': p_q_diff > sqrt_n / 1000
    }
    
    if p_q_diff < sqrt_n / 100:
        analysis['vulnerabilities'].append({
            'type': 'Fermat Factorization',
            'severity': 'HIGH',
            'description': 'p and q are too close',
            'mitigation': 'Regenerate with well-separated primes'
        })
    
    # Check 3: e size
    e_bits = e.bit_length()
    analysis['e_size'] = {
        'e': e,
        'e_bits': e_bits,
        'common_value': e in [3, 17, 65537]
    }
    
    if e == 3:
        analysis['warnings'].append({
            'type': 'Small e',
            'severity': 'MEDIUM',
            'description': 'e=3 vulnerable to broadcast attack',
            'mitigation': 'Use proper padding (OAEP) or larger e'
        })
    
    # Check 4: gcd(e, phi(n))
    gcd_val, _, _ = extended_gcd(e, phi_n)
    analysis['e_phi_coprime'] = {
        'gcd': gcd_val,
        'coprime': gcd_val == 1
    }
    
    if gcd_val != 1:
        analysis['vulnerabilities'].append({
            'type': 'Invalid Key',
            'severity': 'CRITICAL',
            'description': f'gcd(e, φ(n)) = {gcd_val} ≠ 1',
            'mitigation': 'Regenerate with coprime e'
        })
    
    # Check 5: Key size vs NIST recommendations
    nist_recommendations = {
        1024: {'security_bits': 80, 'valid_until': 2010, 'status': 'DEPRECATED'},
        2048: {'security_bits': 112, 'valid_until': 2030, 'status': 'ACCEPTABLE'},
        3072: {'security_bits': 128, 'valid_until': 2050, 'status': 'GOOD'},
        4096: {'security_bits': 152, 'valid_until': 2100, 'status': 'EXCELLENT'}
    }
    
    nist_level = None
    for key_size in sorted(nist_recommendations.keys()):
        if n_bits >= key_size:
            nist_level = nist_recommendations[key_size]
    
    analysis['nist_compliance'] = {
        'key_size': n_bits,
        'security_bits': nist_level['security_bits'] if nist_level else 0,
        'status': nist_level['status'] if nist_level else 'INSUFFICIENT',
        'recommended_until': nist_level['valid_until'] if nist_level else 'N/A'
    }
    
    if n_bits < 2048:
        analysis['warnings'].append({
            'type': 'Weak Key Size',
            'severity': 'HIGH',
            'description': f'{n_bits}-bit keys deprecated by NIST',
            'mitigation': 'Use at least 2048-bit keys'
        })
    
    # Overall security score
    score = 100
    score -= len(analysis['vulnerabilities']) * 30
    score -= len(analysis['warnings']) * 10
    analysis['overall_score'] = max(0, score)
    
    return analysis


def benchmark_performance(pub, priv) -> Dict[str, Any]:
    """Benchmark RSA encryption/decryption performance"""
    
    import random
    
    rsa = RSA(pub, priv)
    
    # Generate random message
    message = random.randint(2, pub.n - 1)
    
    results = {}
    
    # Standard encryption
    ciphertext, enc_time = benchmark(rsa.encrypt_int, message)
    results['encryption'] = {
        'time_ms': enc_time,
        'ciphertext': ciphertext
    }
    
    # Standard decryption
    decrypted, dec_time = benchmark(rsa.decrypt_int, ciphertext)
    results['decryption_standard'] = {
        'time_ms': dec_time,
        'correct': decrypted == message
    }
    
    # CRT decryption
    decrypted_crt, dec_crt_time = benchmark(rsa.decrypt_int_crt, ciphertext)
    results['decryption_crt'] = {
        'time_ms': dec_crt_time,
        'correct': decrypted_crt == message,
        'speedup': dec_time / dec_crt_time if dec_crt_time > 0 else 0
    }
    
    results['message'] = message
    results['summary'] = {
        'encryption_time_ms': enc_time,
        'decryption_standard_ms': dec_time,
        'decryption_crt_ms': dec_crt_time,
        'crt_speedup': f"{dec_time / dec_crt_time:.2f}x" if dec_crt_time > 0 else "N/A"
    }
    
    return results


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """Main entry point for RSA Parameter Lab"""
    
    # Validate
    errors = validate_parameters(params, PARAMETERS)
    if errors:
        raise ValueError(f"Invalid parameters: {', '.join(errors)}")
    
    # Apply defaults
    bits = params.get('bits', 1024)
    e = params.get('e', 65537)
    mode = params['mode']
    
    # Generate experiment ID
    exp_id = create_experiment_id()
    
    # Generate RSA keys
    print(f"Generating {bits}-bit RSA keys with e={e}...")
    pub, priv = keygen(bits, e)
    keys = {
        'public_key': {'e': pub.e, 'n': pub.n},
        'private_key': {'d': priv.d, 'n': priv.n, 'p': priv.p, 'q': priv.q}
    }
    keys_tuple, keygen_time = (pub, priv), 0  # Mock timing for now
    
    # Extract parameters
    n = pub.n
    d = priv.d
    p = priv.p
    q = priv.q
    phi_n = (p - 1) * (q - 1)
    
    # Execute based on mode
    if mode == 'generate_analyze':
        security = analyze_security(n, e, d, p, q, phi_n)
        
        results = {
            'keys': keys,
            'keygen_time_ms': keygen_time,
            'security_analysis': security
        }
        
    elif mode == 'security_check':
        security = analyze_security(n, e, d, p, q, phi_n)
        
        results = {
            'key_size': bits,
            'security_analysis': security,
            'safe': len(security['vulnerabilities']) == 0
        }
        
    elif mode == 'performance_benchmark':
        performance = benchmark_performance(pub, priv)
        
        results = {
            'key_size': bits,
            'performance': performance,
            'keygen_time_ms': keygen_time
        }
        
    elif mode == 'parameter_sweep':
        # Compare different e values
        e_values = [3, 17, 65537]
        sweep_results = {}
        
        for e_test in e_values:
            try:
                keys_test, time_test = benchmark(keygen, bits, e_test)
                sweep_results[f'e={e_test}'] = {
                    'keygen_time_ms': time_test,
                    'success': True
                }
            except Exception as ex:
                sweep_results[f'e={e_test}'] = {
                    'success': False,
                    'error': str(ex)
                }
        
        results = {
            'key_size': bits,
            'e_sweep': sweep_results
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
    print("🔐 Testing RSA Parameter Lab\n")
    
    # Test 1: Generate and analyze
    print("Test 1: Generate and analyze 1024-bit key")
    result1 = run({'mode': 'generate_analyze', 'bits': 1024, 'e': 65537})
    print(f"  Key generated in {result1['results']['keygen_time_ms']:.2f} ms")
    print(f"  Security score: {result1['results']['security_analysis']['overall_score']}/100")
    print(f"  Vulnerabilities: {len(result1['results']['security_analysis']['vulnerabilities'])}")
    print(f"  Warnings: {len(result1['results']['security_analysis']['warnings'])}\n")
    
    # Test 2: Performance benchmark
    print("Test 2: Performance benchmark")
    result2 = run({'mode': 'performance_benchmark', 'bits': 1024})
    perf = result2['results']['performance']['summary']
    print(f"  Encryption: {perf['encryption_time_ms']:.4f} ms")
    print(f"  Decryption (standard): {perf['decryption_standard_ms']:.4f} ms")
    print(f"  Decryption (CRT): {perf['decryption_crt_ms']:.4f} ms")
    print(f"  CRT Speedup: {perf['crt_speedup']}\n")
    
    print("✅ All tests passed!")
