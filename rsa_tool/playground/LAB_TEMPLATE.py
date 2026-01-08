"""
📋 Playground Lab Template

Copy this template to create new playground labs.
Follow this structure for consistency across all labs.

Filename pattern: {topic}_lab.py
Examples: modular_lab.py, exponentiation_lab.py, factorization_lab.py
"""

from typing import Dict, Any
from .playground_utils import (
    create_experiment_id,
    format_results,
    benchmark,
    validate_parameters,
    create_step_log,
    add_step
)

# ============================================================================
# LAB METADATA (Required)
# ============================================================================

NAME = "Template Lab"
DESCRIPTION = "Short one-line description of this lab"
LONG_DESCRIPTION = """
Detailed description of what this lab does.
Explain the algorithms, research questions, and use cases.
Reference CLRS sections if applicable.
"""

PHASE = 1  # 1, 2, 3, or 4 (from roadmap)
CLRS_SECTIONS = ["31.x", "31.y"]  # CLRS chapter sections covered
STATUS = "development"  # 'planning', 'development', 'testing', 'production'

# ============================================================================
# PARAMETER SCHEMA (Required)
# ============================================================================

PARAMETERS = {
    'param1': {
        'type': int,
        'required': True,
        'min': 1,
        'max': 1000,
        'default': 100,
        'description': 'Description of parameter 1'
    },
    'param2': {
        'type': str,
        'required': False,
        'default': 'option1',
        'choices': ['option1', 'option2', 'option3'],
        'description': 'Description of parameter 2'
    },
    # Add more parameters as needed
}

# ============================================================================
# OUTPUT FORMAT (Required)
# ============================================================================

OUTPUT_FORMAT = {
    'result1': {
        'type': 'number',
        'description': 'Description of result 1'
    },
    'result2': {
        'type': 'array',
        'description': 'Description of result 2'
    },
    'steps': {
        'type': 'array',
        'description': 'Step-by-step algorithm execution'
    },
    'benchmark': {
        'type': 'object',
        'description': 'Performance metrics'
    },
    # Add more output fields as needed
}

# ============================================================================
# EXAMPLES (Required)
# ============================================================================

EXAMPLES = [
    {
        'name': 'Basic Example',
        'description': 'Simple use case',
        'parameters': {
            'param1': 42,
            'param2': 'option1'
        },
        'expected_output': {
            'result1': 123,
            'result2': [1, 2, 3]
        }
    },
    # Add more examples
]

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def algorithm_implementation(param1: int, param2: str) -> Dict[str, Any]:
    """
    Main algorithm implementation
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Dictionary with results and intermediate data
    """
    # Step log for visualization
    steps = create_step_log()
    
    # TODO: Implement your algorithm here
    add_step(steps, "Initialize variables", {'param1': param1, 'param2': param2})
    
    # ... algorithm logic ...
    
    add_step(steps, "Complete computation", {'result': 'example'})
    
    return {
        'result1': 123,  # Replace with actual result
        'result2': [1, 2, 3],  # Replace with actual result
        'steps': steps
    }


def comparison_experiment(param1: int) -> Dict[str, Any]:
    """
    Compare multiple approaches/algorithms
    
    Args:
        param1: Common parameter for comparison
        
    Returns:
        Comparison results with benchmarks
    """
    results = {}
    
    # Algorithm 1
    result1, time1 = benchmark(algorithm_implementation, param1, 'option1')
    results['algorithm1'] = {
        'result': result1,
        'time_ms': time1
    }
    
    # Algorithm 2
    result2, time2 = benchmark(algorithm_implementation, param1, 'option2')
    results['algorithm2'] = {
        'result': result2,
        'time_ms': time2
    }
    
    # Comparison metrics
    speedup = time2 / time1 if time1 > 0 else 0
    results['comparison'] = {
        'speedup': speedup,
        'winner': 'algorithm1' if time1 < time2 else 'algorithm2'
    }
    
    return results


# ============================================================================
# MAIN ENTRY POINT (Required)
# ============================================================================

def run(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entry point for the playground lab
    
    This function is called by PlaygroundService.execute()
    
    Args:
        params: Dictionary of parameters from user/API
        
    Returns:
        Standardized result dictionary with:
        - experiment_id
        - timestamp
        - lab name
        - parameters used
        - results
        - metadata
        
    Raises:
        ValueError: If parameters are invalid
    """
    # Validate parameters
    errors = validate_parameters(params, PARAMETERS)
    if errors:
        raise ValueError(f"Invalid parameters: {', '.join(errors)}")
    
    # Apply defaults for missing optional parameters
    for param_name, schema in PARAMETERS.items():
        if param_name not in params and 'default' in schema:
            params[param_name] = schema['default']
    
    # Generate experiment ID
    exp_id = create_experiment_id()
    
    # Extract parameters
    param1 = params.get('param1')
    param2 = params.get('param2')
    mode = params.get('mode', 'single')  # 'single' or 'comparison'
    
    # Execute based on mode
    if mode == 'single':
        algo_result, time_ms = benchmark(algorithm_implementation, param1, param2)
        results = {
            'algorithm_result': algo_result,
            'benchmark': {
                'time_ms': time_ms,
                'operations': algo_result.get('operations', 0)
            }
        }
    elif mode == 'comparison':
        results = comparison_experiment(param1)
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
# HELPER FUNCTIONS (Optional)
# ============================================================================

def visualize_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate visualization data for frontend
    
    Args:
        results: Results from run()
        
    Returns:
        Visualization configuration (charts, graphs, tables)
    """
    # TODO: Implement visualization logic
    return {
        'charts': [],
        'tables': [],
        'graphs': []
    }


# ============================================================================
# TESTING (Optional but recommended)
# ============================================================================

if __name__ == "__main__":
    # Quick test
    test_params = {
        'param1': 42,
        'param2': 'option1',
        'mode': 'single'
    }
    
    print("Testing Template Lab...")
    result = run(test_params)
    print(f"Experiment ID: {result['experiment_id']}")
    print(f"Results: {result['results']}")
    print("✅ Test passed!")
