# 🔬 Playground Module - Phòng Thí Nghiệm Nghiên Cứu

**Tác giả:** Đỗ Văn Tài  
**Mục đích:** Môi trường thử nghiệm thuật toán và thu thập dữ liệu nghiên cứu  

---

## 📖 Giới Thiệu

Playground Module là hệ thống **7 phòng thí nghiệm (labs)** cho phép người dùng:
- ✅ Thử nghiệm các thuật toán số học và mật mã
- ✅ So sánh hiệu năng giữa các thuật toán
- ✅ Thu thập dữ liệu để phân tích và viết báo cáo
- ✅ Xuất kết quả dạng JSON để xử lý thêm
- ✅ Phát hiện lỗ hổng bảo mật trong cấu hình RSA

---

## 📁 Cấu Trúc Labs

Các labs được tổ chức theo 4 phase từ cơ bản đến nâng cao:

```
playground/
├── __init__.py              # PlaygroundService - điều phối các labs
├── playground_utils.py      # Công cụ chung: benchmark, format, validate
├── LAB_TEMPLATE.py          # Template chuẩn để tạo labs mới
│
└── labs/
    ├── phase1/              # Phase 1: Lý thuyết số cơ bản (CLRS 31.1-31.6)
    │   ├── modular_lab.py         # Số học modulo, GCD, CRT
    │   └── exponentiation_lab.py  # Lũy thừa, order, căn nguyên thủy
    │
    ├── phase2/              # Phase 2: Số nguyên tố & RSA (CLRS 31.7-31.8)
    │   ├── prime_lab.py           # Miller-Rabin, Fermat, Trial Division
    │   └── rsa_parameter_lab.py   # Phân tích tham số RSA
    │
    ├── phase3/              # Phase 3: Phân tích mật mã (CLRS 31.9)
    │   ├── factorization_lab.py   # Pollard Rho, Fermat factorization
    │   └── rsa_attacks_lab.py     # Wiener, Common Modulus, Broadcast
    │
    └── phase4/              # Phase 4: Chủ đề nâng cao (Beyond CLRS)
        └── discrete_log_lab.py    # DLP, Diffie-Hellman, ElGamal
```

**Giá trị của cấu trúc phase:**
- 📚 Học tập theo lộ trình từ cơ bản → nâng cao
- 🎯 Dễ theo dõi tiến độ
- 🔄 Mỗi phase độc lập, có thể học riêng lẻ

## 🎯 Cách Sử Dụng

### 1. Sử Dụng Trong Python Code

```python
from rsa_tool.playground import PlaygroundService

# Liệt kê tất cả labs có sẵn
labs = PlaygroundService.list_all()
for lab in labs:
    print(f"- {lab['name']} (Phase {lab['phase']})")

# Lấy thông tin chi tiết về 1 lab
info = PlaygroundService.get_lab_info('modular_arithmetic')
print(f"Parameters: {info['parameters']}")
print(f"Examples: {info['examples']}")

# Thực thi một lab với tham số
params = {
    'mode': 'extended_gcd',
    'a': 240,
    'b': 46
}
result = PlaygroundService.execute('modular_arithmetic', params)
print(result)
```

### 2. Sử Dụng Qua Web API

```bash
# List all labs
curl http://127.0.0.1:5000/api/playground/list

# Get lab info
curl http://127.0.0.1:5000/api/playground/info/modular_arithmetic

# Run a lab
curl -X POST http://127.0.0.1:5000/api/playground/run \
  -H "Content-Type: application/json" \
  -d '{
    "lab_id": "modular_arithmetic",
    "parameters": {
      "mode": "extended_gcd",
      "a": 240,
      "b": 46
    }
  }'
```

### 3. Test Labs Trực Tiếp

Mỗi lab có thể chạy độc lập để test:

```bash
# Test Modular Arithmetic Lab
python -m rsa_tool.playground.labs.phase1.modular_lab

# Test Discrete Logarithm Lab
python -m rsa_tool.playground.labs.phase4.discrete_log_lab
```
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

---

## 💡 Giá Trị và Lợi Ích

### Cho Sinh Viên 📚
- Học lý thuyết số qua thực hành
- Thấy cách thuật toán hoạt động step-by-step
- So sánh hiệu năng các thuật toán

### Cho Nhà Nghiên Cứu 🔬
- Môi trường thử nghiệm có sẵn
- Thu thập dữ liệu JSON để phân tích
- Benchmark chính xác

### Cho Giảng Viên 👨‍🏫
- Dạy CLRS Chapter 31 với demos trực quan
- Cho bài tập thực hành
- Đánh giá hiểu biết sinh viên

---

## 📚 Tài Liệu Tham Khảo

- **CLRS Chapter 31**: Number-Theoretic Algorithms
- **demos/**: Các ví dụ implementation
- **Algorithms/**: Core number theory functions
- **RESEARCH_ROADMAP.md**: Kế hoạch dự án đầy đủ

---

## 👨‍💻 Thông Tin

**Tác giả:** Đỗ Văn Tài  
**Email:** lucdoka1245@gmail.com  
**Mục đích:** Nghiên cứu và giáo dục mật mã học  

**Last Updated:** January 8, 2026  
**Status:** ✅ 7 Labs Complete (Phase 1-4)
