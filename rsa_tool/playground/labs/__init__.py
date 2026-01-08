"""
Labs organized by phases from RESEARCH_ROADMAP.md
"""

# Phase 1: Core Number Theory
from .phase1 import modular_lab

# Phase 2: Primality & RSA
from .phase2 import prime_lab, rsa_parameter_lab

# Phase 3: Cryptanalysis (future)
# from .phase3 import factorization_lab, rsa_attacks_lab

__all__ = [
    'modular_lab',
    'prime_lab',
    'rsa_parameter_lab',
]
