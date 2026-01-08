"""
🧮 Playground Utilities

Shared utilities for all playground modules including:
- Data formatting and export
- Visualization helpers
- Mathematical utilities
- Benchmark tools
"""

import json
import time
from typing import Any, Dict, List, Callable
from datetime import datetime


def create_experiment_id() -> str:
    """Generate unique experiment ID with timestamp"""
    return f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def format_results(
    experiment_id: str,
    lab_name: str,
    parameters: Dict[str, Any],
    results: Dict[str, Any],
    metadata: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Standardize result format for all labs
    
    Args:
        experiment_id: Unique experiment identifier
        lab_name: Name of the lab module
        parameters: Input parameters
        results: Lab-specific results
        metadata: Optional metadata
        
    Returns:
        Standardized result dictionary
    """
    return {
        'experiment_id': experiment_id,
        'timestamp': datetime.now().isoformat(),
        'lab': lab_name,
        'parameters': parameters,
        'results': results,
        'metadata': metadata or {},
        'version': '1.0.0'
    }


def benchmark(func: Callable, *args, **kwargs) -> tuple[Any, float]:
    """
    Benchmark a function execution
    
    Args:
        func: Function to benchmark
        *args, **kwargs: Function arguments
        
    Returns:
        Tuple of (result, time_ms)
    """
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    time_ms = (end_time - start_time) * 1000
    return result, time_ms


def export_to_json(data: Dict[str, Any], pretty: bool = True) -> str:
    """
    Export data to JSON string
    
    Args:
        data: Data to export
        pretty: Pretty print with indentation
        
    Returns:
        JSON string
    """
    if pretty:
        return json.dumps(data, indent=2, ensure_ascii=False)
    return json.dumps(data, ensure_ascii=False)


def export_to_csv(data: List[Dict[str, Any]], columns: List[str] = None) -> str:
    """
    Export data to CSV string
    
    Args:
        data: List of dictionaries
        columns: Column order (default: keys from first row)
        
    Returns:
        CSV string
    """
    if not data:
        return ""
    
    if columns is None:
        columns = list(data[0].keys())
    
    # Header
    csv_lines = [','.join(columns)]
    
    # Rows
    for row in data:
        values = [str(row.get(col, '')) for col in columns]
        csv_lines.append(','.join(values))
    
    return '\n'.join(csv_lines)


def format_number(n: int, notation: str = 'default') -> str:
    """
    Format large numbers for display
    
    Args:
        n: Number to format
        notation: 'default', 'scientific', 'compact'
        
    Returns:
        Formatted string
    """
    if notation == 'scientific':
        return f"{n:.3e}"
    elif notation == 'compact':
        if n < 1000:
            return str(n)
        elif n < 1_000_000:
            return f"{n/1000:.1f}K"
        elif n < 1_000_000_000:
            return f"{n/1_000_000:.1f}M"
        else:
            return f"{n/1_000_000_000:.1f}B"
    else:
        return str(n)


def validate_parameters(params: Dict[str, Any], schema: Dict[str, Dict]) -> List[str]:
    """
    Validate parameters against schema
    
    Args:
        params: Parameters to validate
        schema: Schema dict with keys: {param_name: {type, required, min, max, ...}}
        
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    
    for param_name, rules in schema.items():
        # Check required
        if rules.get('required', False) and param_name not in params:
            errors.append(f"Missing required parameter: {param_name}")
            continue
        
        if param_name not in params:
            continue
        
        value = params[param_name]
        
        # Check type
        expected_type = rules.get('type')
        if expected_type and not isinstance(value, expected_type):
            errors.append(f"Parameter '{param_name}' must be {expected_type.__name__}")
        
        # Check range for numbers
        if isinstance(value, (int, float)):
            if 'min' in rules and value < rules['min']:
                errors.append(f"Parameter '{param_name}' must be >= {rules['min']}")
            if 'max' in rules and value > rules['max']:
                errors.append(f"Parameter '{param_name}' must be <= {rules['max']}")
    
    return errors


def create_step_log() -> List[Dict[str, Any]]:
    """Create empty step log for algorithm visualization"""
    return []


def add_step(log: List[Dict[str, Any]], description: str, data: Dict[str, Any] = None):
    """
    Add a step to algorithm visualization log
    
    Args:
        log: Step log list
        description: Step description
        data: Optional data for this step
    """
    log.append({
        'step': len(log) + 1,
        'description': description,
        'data': data or {}
    })


def create_comparison_table(
    algorithms: List[str],
    metrics: List[str],
    results: Dict[str, Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Create comparison table for multiple algorithms
    
    Args:
        algorithms: List of algorithm names
        metrics: List of metric names
        results: Nested dict {algorithm: {metric: value}}
        
    Returns:
        Table structure for frontend rendering
    """
    table = {
        'headers': ['Algorithm'] + metrics,
        'rows': []
    }
    
    for algo in algorithms:
        row = [algo]
        for metric in metrics:
            value = results.get(algo, {}).get(metric, 'N/A')
            row.append(value)
        table['rows'].append(row)
    
    return table


# Constants for common use
TOOL_VERSION = "1.0.0"
SUPPORTED_EXPORT_FORMATS = ['json', 'csv']
