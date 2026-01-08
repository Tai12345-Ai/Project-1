"""
🔬 Research Playground Modules

Interactive labs for academic research on Number-Theoretic Algorithms (CLRS Chapter 31).

Available Modules:
- modular_lab: Modular arithmetic equations, Extended Euclidean, CRT
- exponentiation_lab: Algorithm comparison, order computation, primitive roots
- prime_lab: Multi-algorithm primality testing, distribution analysis
- rsa_parameter_lab: Security analysis, configuration optimization
- factorization_lab: Multi-algorithm factorization, attack simulation
- rsa_attacks_lab: Wiener, broadcast, timing, padding oracle attacks

Usage:
    from rsa_tool.playground import PlaygroundService
    
    # List all available labs
    labs = PlaygroundService.list_all()
    
    # Execute a lab
    result = PlaygroundService.execute('modular_arithmetic', params)
"""

from typing import Dict, List, Any


class PlaygroundService:
    """Coordinator for research playground modules"""
    
    # Registry of available labs (will be populated as modules are implemented)
    _LABS = {}
    
    @classmethod
    def register_lab(cls, lab_id: str, lab_module):
        """
        Register a new playground lab
        
        Args:
            lab_id: Unique identifier for the lab
            lab_module: Module containing run() function
        """
        cls._LABS[lab_id] = lab_module
    
    @classmethod
    def list_all(cls) -> List[Dict[str, Any]]:
        """
        Get list of all available playground labs
        
        Returns:
            List of lab metadata dictionaries
        """
        labs = []
        for lab_id, module in cls._LABS.items():
            labs.append({
                'id': lab_id,
                'name': getattr(module, 'NAME', lab_id),
                'description': getattr(module, 'DESCRIPTION', ''),
                'phase': getattr(module, 'PHASE', 'unknown'),
                'clrs_sections': getattr(module, 'CLRS_SECTIONS', []),
                'status': getattr(module, 'STATUS', 'development')
            })
        return labs
    
    @classmethod
    def execute(cls, lab_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a playground lab with given parameters
        
        Args:
            lab_id: Lab identifier
            params: Lab-specific parameters
            
        Returns:
            Lab results including data, visualizations, export info
            
        Raises:
            ValueError: If lab_id not found
        """
        if lab_id not in cls._LABS:
            raise ValueError(f"Lab '{lab_id}' not found. Available: {list(cls._LABS.keys())}")
        
        module = cls._LABS[lab_id]
        if not hasattr(module, 'run'):
            raise AttributeError(f"Lab module '{lab_id}' missing run() function")
        
        return module.run(params)
    
    @classmethod
    def get_lab_info(cls, lab_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific lab
        
        Args:
            lab_id: Lab identifier
            
        Returns:
            Lab metadata and parameter schema
        """
        if lab_id not in cls._LABS:
            raise ValueError(f"Lab '{lab_id}' not found")
        
        module = cls._LABS[lab_id]
        
        # Convert parameters to JSON-serializable format
        parameters = getattr(module, 'PARAMETERS', {})
        serializable_params = {}
        for param_name, param_schema in parameters.items():
            serializable_schema = {}
            for key, value in param_schema.items():
                if key == 'type':
                    # Convert type objects to string
                    if value == int:
                        serializable_schema[key] = 'int'
                    elif value == str:
                        serializable_schema[key] = 'str'
                    elif value == bool:
                        serializable_schema[key] = 'bool'
                    elif value == list:
                        serializable_schema[key] = 'list'
                    else:
                        serializable_schema[key] = str(value.__name__)
                else:
                    serializable_schema[key] = value
            serializable_params[param_name] = serializable_schema
        
        return {
            'id': lab_id,
            'name': getattr(module, 'NAME', lab_id),
            'description': getattr(module, 'DESCRIPTION', ''),
            'long_description': getattr(module, 'LONG_DESCRIPTION', ''),
            'phase': getattr(module, 'PHASE', 'unknown'),
            'clrs_sections': getattr(module, 'CLRS_SECTIONS', []),
            'parameters': serializable_params,
            'output_format': getattr(module, 'OUTPUT_FORMAT', {}),
            'examples': getattr(module, 'EXAMPLES', []),
            'status': getattr(module, 'STATUS', 'development')
        }


# Import and register implemented labs
from . import modular_lab
PlaygroundService.register_lab('modular_arithmetic', modular_lab)

# TODO: Future labs (implement as needed)
# from . import exponentiation_lab
# PlaygroundService.register_lab('exponentiation', exponentiation_lab)

# from . import prime_lab
# PlaygroundService.register_lab('primality', prime_lab)

# from . import rsa_parameter_lab
# PlaygroundService.register_lab('rsa_parameters', rsa_parameter_lab)

# from . import factorization_lab
# PlaygroundService.register_lab('factorization', factorization_lab)

# from . import rsa_attacks_lab
# PlaygroundService.register_lab('rsa_attacks', rsa_attacks_lab)


__all__ = ['PlaygroundService']
