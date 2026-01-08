# 🔬 Playground Module - README

## 📁 Structure

```
playground/
├── __init__.py              # PlaygroundService coordinator
├── playground_utils.py      # Shared utilities
├── LAB_TEMPLATE.py          # Template for new labs
│
├── modular_lab.py          # Phase 1.1 - Modular Arithmetic
├── exponentiation_lab.py   # Phase 1.2 - Exponentiation & Order
├── prime_lab.py            # Phase 2.1 - Primality Testing
├── rsa_parameter_lab.py    # Phase 2.2 - RSA Parameters
├── factorization_lab.py    # Phase 3.1 - Factorization
└── rsa_attacks_lab.py      # Phase 3.2 - RSA Attacks
```

## 🎯 Usage

### From Python Code

```python
from rsa_tool.playground import PlaygroundService

# List all available labs
labs = PlaygroundService.list_all()
print(labs)

# Get detailed info about a lab
info = PlaygroundService.get_lab_info('modular_arithmetic')
print(info['parameters'])

# Execute a lab
params = {
    'a': 5,
    'b': 3,
    'm': 7
}
result = PlaygroundService.execute('modular_arithmetic', params)
print(result['results'])

# Export to JSON
import json
with open('experiment.json', 'w') as f:
    json.dump(result, f, indent=2)
```

### From Flask API

```python
# In app_simple.py
from rsa_tool.playground import PlaygroundService

@app.route('/api/playground/<lab_id>', methods=['GET'])
def playground_info(lab_id):
    info = PlaygroundService.get_lab_info(lab_id)
    return jsonify(info)

@app.route('/api/playground/<lab_id>/run', methods=['POST'])
def playground_run(lab_id):
    params = request.json
    result = PlaygroundService.execute(lab_id, params)
    return jsonify(result)
```

### From Frontend (JavaScript)

```javascript
// Get lab info
fetch('/api/playground/modular_arithmetic')
  .then(r => r.json())
  .then(info => {
    console.log('Parameters:', info.parameters);
    console.log('Examples:', info.examples);
  });

// Run experiment
fetch('/api/playground/modular_arithmetic/run', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    a: 5,
    b: 3,
    m: 7
  })
})
  .then(r => r.json())
  .then(result => {
    console.log('Experiment ID:', result.experiment_id);
    console.log('Results:', result.results);
    // Download as JSON
    const blob = new Blob([JSON.stringify(result, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${result.experiment_id}.json`;
    a.click();
  });
```

## 📝 Creating a New Lab

### Step 1: Copy Template

```bash
cd rsa_tool/playground
cp LAB_TEMPLATE.py your_new_lab.py
```

### Step 2: Fill in Metadata

```python
NAME = "Your Lab Name"
DESCRIPTION = "One-line description"
PHASE = 1  # or 2, 3, 4
CLRS_SECTIONS = ["31.x"]
STATUS = "development"
```

### Step 3: Define Parameters

```python
PARAMETERS = {
    'param1': {
        'type': int,
        'required': True,
        'min': 1,
        'max': 1000,
        'default': 100,
        'description': 'What this parameter controls'
    }
}
```

### Step 4: Implement Logic

```python
def run(params: Dict[str, Any]) -> Dict[str, Any]:
    # Validate
    errors = validate_parameters(params, PARAMETERS)
    if errors:
        raise ValueError(errors)
    
    # Your algorithm here
    result = your_algorithm(params['param1'])
    
    # Return standardized format
    return format_results(
        experiment_id=create_experiment_id(),
        lab_name=NAME,
        parameters=params,
        results=result
    )
```

### Step 5: Register in __init__.py

```python
# In playground/__init__.py
from . import your_new_lab
PlaygroundService.register_lab('your_lab_id', your_new_lab)
```

### Step 6: Test

```bash
cd rsa_tool/playground
python your_new_lab.py
```

## 🎨 UI Guidelines

Each lab should provide data suitable for:

### 1. **Interactive Controls**
```python
# Parameter ranges → sliders/inputs in UI
PARAMETERS = {
    'bits': {'type': int, 'min': 8, 'max': 2048}  # → Slider
}
```

### 2. **Real-time Results**
```python
# Fast computations (< 1s) → live updates
# Slow computations → progress indicator
```

### 3. **Visualizations**
```python
results = {
    'chart_data': {
        'type': 'line',
        'x': [1, 2, 3, 4],
        'y': [10, 20, 15, 25],
        'title': 'Performance vs Input Size'
    }
}
```

### 4. **Step-by-Step**
```python
steps = [
    {'step': 1, 'description': 'Initialize', 'data': {...}},
    {'step': 2, 'description': 'Compute', 'data': {...}}
]
```

### 5. **Export Options**
```python
# Automatic JSON export
# Optional: CSV for tabular data
# Optional: LaTeX for papers
```

## 📊 Output Standards

All labs must return this structure:

```python
{
    "experiment_id": "exp_20260108_143522",
    "timestamp": "2026-01-08T14:35:22.123456",
    "lab": "Modular Arithmetic Lab",
    "parameters": {
        "a": 5,
        "b": 3,
        "m": 7
    },
    "results": {
        # Lab-specific results
        "solution": 2,
        "steps": [...],
        "benchmark": {
            "time_ms": 0.42,
            "operations": 5
        }
    },
    "metadata": {
        "clrs_sections": ["31.1", "31.2"],
        "phase": 1,
        "status": "production",
        "version": "1.0.0"
    }
}
```

## 🧪 Testing Checklist

Before marking lab as "production":

- [ ] Parameter validation works
- [ ] All required fields in output
- [ ] Benchmark timing accurate
- [ ] Step-by-step logs correct
- [ ] Edge cases handled
- [ ] Error messages clear
- [ ] Examples run successfully
- [ ] Export to JSON works
- [ ] Documentation complete
- [ ] Unit tests pass (if any)

## 🔗 Integration with Demos

Demos vs Playgrounds:

| Feature | Demos | Playgrounds |
|---------|-------|-------------|
| Purpose | Show how it works | Research tool |
| Interactivity | Fixed examples | Full parameter control |
| Output | Text explanation | Data export |
| Audience | Learning | Research |
| Complexity | Simple | Advanced |

Example: Reusing demo code in playground:

```python
# In playground/factorization_lab.py
from Algorithms.pollard_rho import pollard_rho  # Reuse existing code

def run(params):
    n = params['n']
    result, time_ms = benchmark(pollard_rho, n)
    return format_results(...)
```

## 📚 Resources

- **CLRS Chapter 31**: Algorithm reference
- **demos/**: Example implementations
- **Algorithms/**: Core number theory functions
- **RESEARCH_ROADMAP.md**: Full project plan

## 🚀 Next Steps

1. Implement `modular_lab.py` (Week 1)
2. Implement `exponentiation_lab.py` (Week 2)
3. Add API routes to `app_simple.py`
4. Create frontend "Playground" tab
5. Test data export workflow
6. Iterate based on feedback

---

**Status:** 📋 Planning → 🚧 Ready for Implementation  
**Priority:** Modular Lab (Phase 1.1) first!
