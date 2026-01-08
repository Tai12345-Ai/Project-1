"""
🧪 Playground Labs Collection

Each phase represents a progressive research module in cryptography and number theory.

Available Labs:
- Phase 1: Linear Congruence & Extended GCD
- Phase 2: Chinese Remainder Theorem & Advanced Modular Arithmetic
- Phase 3: Modular Exponentiation & Primality Testing
- Phase 4: RSA Cryptosystem Components
"""

from . import phase_01_linear_congruence
from . import phase_02_crt_advanced
from . import phase_03_exponentiation
from . import phase_04_rsa_components

__all__ = [
    'phase_01_linear_congruence',
    'phase_02_crt_advanced',
    'phase_03_exponentiation',
    'phase_04_rsa_components'
]

# Lab registry for dynamic loading
LABS = {
    1: phase_01_linear_congruence,
    2: phase_02_crt_advanced,
    3: phase_03_exponentiation,
    4: phase_04_rsa_components
}

def get_lab(phase: int):
    """Get lab module by phase number"""
    return LABS.get(phase)

def list_labs():
    """List all available labs with metadata"""
    return [
        {
            'phase': phase,
            'name': lab.NAME,
            'description': lab.DESCRIPTION,
            'status': lab.STATUS,
            'clrs_sections': lab.CLRS_SECTIONS
        }
        for phase, lab in LABS.items()
    ]
