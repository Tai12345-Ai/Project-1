# 🔐 RSA Cryptography Research Tool

**Interactive web platform for studying Number-Theoretic Algorithms (CLRS Chapter 31)**

Công cụ web minh họa thuật toán RSA từ CLRS Chương 31 với 8 demos chi tiết và research playgrounds.

## 🎯 Features

- **8 Interactive Demos** - From RSA basics to advanced attacks
- **6 Research Playgrounds** (in development) - Interactive labs for academic research
- **Full CLRS Ch31 Coverage** - Modular arithmetic to RSA cryptanalysis
- **Data Export** - JSON/CSV for research papers
- **Modular Architecture** - Easy to extend and maintain

👉 **[Research Roadmap](rsa_tool/RESEARCH_ROADMAP.md)** - Detailed implementation plan

## 📁 Kiến trúc Dự án (MODULAR)

```
rsa_tool/
│
├── app_simple.py                    # 🎯 MAIN APPLICATION (Flask Routes)
│   ├── Khởi tạo Flask app
│   ├── Định nghĩa API endpoints
│   ├── Gọi services xử lý logic
│   └── Trả về JSON responses
│
├── services/                        # 🔧 BUSINESS LOGIC (Modular)
│   ├── __init__.py                  # Package exports
│   └── rsa_service.py               # RSAService class
│       ├── generate_keys()          - Sinh cặp khóa RSA
│       ├── encrypt()                - Mã hóa message
│       ├── decrypt()                - Giải mã (có CRT option)
│       ├── sign()                   - Ký số message
│       └── verify()                 - Xác minh chữ ký
│
├── demos/                           # 🎬 DEMONSTRATIONS (8 Demos - Easy to Manage)
│   ├── __init__.py                  # DemoService coordinator
│   ├── demo_utils.py                # Shared imports & utilities
│   ├── demo_01_basic_rsa.py         ✓ RSA cơ bản (REFACTORED)
│   ├── demo_02_miller_rabin.py      - Primality test chi tiết
│   ├── demo_03_crt_speed.py         - CRT optimization
│   ├── demo_04_pollard_rho.py       - Factorization attack
│   ├── demo_05_textbook_padding.py  - Security vulnerabilities
│   ├── demo_06_wiener_attack.py     - Attack RSA với d nhỏ
│   ├── demo_07_key_size_security.py - Key size analysis
│   └── demo_08_rsa_properties.py    - Mathematical properties
│
└── templates/
    └── index.html                   # 📄 FRONTEND (Single Page Application)
        ├── HTML structure
        ├── Embedded CSS
        ├── Embedded JavaScript
        └── API calls to backend
```

## 🎯 Ý Nghĩa Từng File

### 1. `app_simple.py` - Application Layer
**Trách nhiệm:** HTTP request/response handling

```python
# Ví dụ route
@app.route('/api/key/generate', methods=['POST'])
def generate_key():
    data = request.json
    bits = int(data.get('bits', 1024))
    
    # Gọi service xử lý
    result = RSAService.generate_keys(bits=bits)
    
    return jsonify({'success': True, 'data': result})
```

**Lợi ích:**
- ✅ Tách biệt HTTP logic khỏi business logic
- ✅ Dễ test (mock services)
- ✅ RESTful API design
- ✅ Có thể thay đổi framework (FastAPI, Django) mà không ảnh hưởng services

### 2. `services/` - Business Logic Layer (MODULAR)
**Trách nhiệm:** RSA operations logic

```
services/
├── __init__.py              # Export RSAService
└── rsa_service.py           # Main RSA logic
```

```python
# services/rsa_service.py
class RSAService:
    @staticmethod
    def generate_keys(bits=1024, e=65537):
        """
        Sinh khóa RSA
        - Gọi Algorithms.rsa.keygen()
        - Format output thành dict
        - Không phụ thuộc Flask
        """
        pub, priv = keygen(bits=bits, e=e)
        return {'public_key': {...}, 'private_key': {...}}
```

**Lợi ích:**
- ✅ Reusable (có thể dùng trong CLI, GUI, API khác)
- ✅ Testable độc lập
- ✅ Single Responsibility Principle
- ✅ Không mix Flask code với crypto code
- ✅ **Dễ thêm services mới** (crypto_service.py, utils_service.py...)

### 3. `demos/` - Demonstration Layer (HIGHLY MODULAR)
**Trách nhiệm:** Educational demonstrations - MỖI DEMO 1 FILE

```
demos/
├── __init__.py                      # DemoService coordinator
├── demo_utils.py                    # Shared imports
├── demo_01_basic_rsa.py            # 150 lines
├── demo_02_miller_rabin.py         # 180 lines
├── demo_03_crt_speed.py            # 200 lines
├── demo_04_pollard_rho.py          # 130 lines
├── demo_05_textbook_padding.py     # 120 lines
├── demo_06_wiener_attack.py        # 90 lines
├── demo_07_key_size_security.py    # 130 lines
└── demo_08_rsa_properties.py       # 150 lines
```

```python
# demos/demo_01_basic_rsa.py
from .demo_utils import *

def demo_basic_rsa():
    """Demo 01: RSA cơ bản"""
    print("╔" + "═" * 78 + "╗")
    print("║   DEMO 01: BASIC RSA   ║")
    # ... demo logic ...
```

**Lợi ích:**
- ✅ **Dễ maintain**: Sửa demo 01 không ảnh hưởng demo 02
- ✅ **Dễ thêm demos mới**: Chỉ cần tạo file mới + import vào __init__.py
- ✅ **Collaboration-friendly**: Nhiều người có thể làm việc cùng lúc
- ✅ **Git-friendly**: Conflicts ít hơn khi merge
- ✅ **Dễ test từng demo**: pytest demos/demo_01_basic_rsa.py
- ✅ **Clear separation**: Mỗi file ~100-200 lines thay vì 1 file 1100+ lines

### 4. `templates/index.html` - Presentation Layer
**Trách nhiệm:** User Interface

- **HTML:** Structure
- **CSS:** Styling (embedded)
- **JavaScript:** Interactivity + API calls

**Lợi ích:**
- ✅ Single Page Application
- ✅ Responsive design
- ✅ Clean separation from backend

## 🎬 8 Demos Chi Tiết

### Demo 01: Basic RSA
- ✅ Step-by-step key generation
- ✅ Mathematical verification (n = p×q, e×d ≡ 1)
- ✅ Multiple message encryption
- ✅ Digital signature với tamper test
- ✅ Deterministic property test

### Demo 02: Miller-Rabin
- ✅ Algorithm explanation
- ✅ Test known primes/composites
- ✅ Probability analysis (error rate)
- ✅ Prime generation performance
- ✅ Compare với Trial Division

### Demo 03: CRT Speed
- ✅ CRT algorithm explanation
- ✅ Performance test (multiple key sizes)
- ✅ Step-by-step CRT calculation
- ✅ Mathematical proof
- ✅ Speedup analysis (~4x)

### Demo 04: Pollard Rho
- ✅ Factorization tests (40-128 bits)
- ✅ Detailed analysis
- ✅ Security implications table
- ✅ Why RSA needs large primes
- ✅ Quantum threat discussion

### Demo 05: Textbook Padding
- ✅ Deterministic vulnerability
- ✅ Homomorphic property attack
- ✅ Malleability demonstration
- ✅ Padding solutions (OAEP, PKCS#1)

### Demo 06: Wiener's Attack
- ✅ Small d vulnerability
- ✅ Continued fraction attack
- ✅ Security threshold (d < n^0.25)
- ✅ Real-world implications

### Demo 07: Key Size Security
- ✅ NIST recommendations table
- ✅ Performance comparison (all key sizes)
- ✅ Historical timeline (factorization records)
- ✅ Future threats (quantum computing)

### Demo 08: RSA Properties
- ✅ Correctness: (m^e)^d ≡ m (mod n)
- ✅ Euler's theorem verification
- ✅ Key relationship: e·d ≡ 1 (mod φ(n))
- ✅ Commutativity (encrypt/decrypt)
- ✅ Homomorphic property
- ✅ CRT efficiency

---

## 🔬 Research Playgrounds (In Development)

**Objective:** Transform from demo tool → research platform for CLRS Chapter 31

### Phase 1: Core Number Theory ✅ Priority
1. **Modular Arithmetic Lab** - Solve equations, Extended Euclidean, CRT
2. **Exponentiation & Order Lab** - Algorithm comparison, primitive roots

### Phase 2: Primality & RSA
3. **Prime & Primality Lab** - Multi-algorithm testing, distribution analysis
4. **RSA Parameter Lab** - Security analysis, configuration optimization

### Phase 3: Cryptanalysis 🔥 Important
5. **Factorization Lab** - Multi-algorithm comparison, attack simulation
6. **RSA Attacks Lab** - Wiener, broadcast, timing, padding oracle attacks

### Phase 4: Advanced (Optional)
7. **Discrete Logarithm Lab** - DLP algorithms, Diffie-Hellman
8. **Lattice-Based Attacks Lab** - Coppersmith, LLL algorithm

📋 **[Full Research Roadmap](rsa_tool/RESEARCH_ROADMAP.md)** - Detailed plan with CLRS mapping

## 🚀 Cách Chạy

```bash
# 1. Activate virtual environment
source .venv/Scripts/activate  # Windows Git Bash
# hoặc
.venv\Scripts\activate         # Windows CMD

# 2. Đảm bảo Flask đã cài
pip install Flask

# 3. Chạy app
cd rsa_tool
python app_simple.py

# 4. Mở browser
http://127.0.0.1:5000
```

## 📊 API Endpoints

### Key Management
```http
POST /api/key/generate
Body: {"bits": 1024, "e": 65537}
```

### Cryptographic Operations
```http
POST /api/crypto/encrypt
POST /api/crypto/decrypt
POST /api/crypto/sign
POST /api/crypto/verify
```

### Demonstrations
```http
GET /api/demo/<demo_name>
GET /api/demo/list
```

## ✨ Điểm Mạnh Của Kiến Trúc

### 1. Separation of Concerns
- **Routes** (app.py) ← HTTP handling
- **Services** (services.py) ← Business logic
- **Demos** (demos.py) ← Educational content
- **Templates** (index.html) ← UI

### 2. Maintainability
- Dễ tìm bug (mỗi file có nhiệm vụ riêng)
- Dễ thêm feature mới
- Dễ refactor

### 3. Testability
- Test services độc lập (không cần Flask)
- Mock services khi test routes
- Unit test từng layer

### 4. Scalability
- Dễ thêm endpoints mới
- Dễ thêm demos mới
- Có thể tách services thành microservices

### 5. Reusability
- Services dùng được cho CLI, GUI, API khác
- Demos có thể chạy standalone
- Template có thể dùng cho mobile app

## 🆚 So Sánh Kiến Trúc

| Aspect | Old (Single File) | New (Modular) |
|--------|------------------|---------------|
| **services.py** | 1 file (151 lines) | Folder: 2 files |
| **demos.py** | 1 file (1136 lines) ❌ | Folder: 10 files (~150 lines each) ✅ |
| **Maintainability** | Khó (scroll nhiều) | Dễ (mỗi file nhỏ) |
| **Collaboration** | Conflict nhiều | Parallel work ✅ |
| **Testing** | Test cả file lớn | Test từng module |
| **Adding Features** | Sửa file lớn | Tạo file mới |
| **Git Diff** | Khó đọc (1000+ lines) | Rõ ràng (<200 lines) |
| **Import Speed** | Load hết (~5MB) | Load on-demand |
| **IDE Performance** | Chậm (file lớn) | Nhanh ✅ |

## ✨ Điểm Mạnh Của Kiến Trúc Mới

### 1. Separation of Concerns
- **Routes** (app.py) ← HTTP handling
- **Services/** (services/) ← Business logic (modular)
- **Demos/** (demos/) ← Educational content (mỗi demo 1 file)
- **Templates** (index.html) ← UI

### 2. Maintainability (IMPROVED)
- ✅ Dễ tìm bug (mỗi file có nhiệm vụ riêng)
- ✅ Dễ thêm feature mới (tạo file mới, không sửa file cũ)
- ✅ Dễ refactor (ảnh hưởng local, không global)
- ✅ **File nhỏ (~150 lines) dễ đọc hơn file lớn (1000+ lines)**

### 3. Testability
- Test services độc lập (không cần Flask)
- Test từng demo riêng biệt
- Mock services khi test routes
- Unit test từng layer

### 4. Scalability
- Dễ thêm endpoints mới
- Dễ thêm demos mới (chỉ cần 1 file)
- Có thể tách services thành microservices
- **Load on-demand** (không load hết 8 demos nếu chỉ cần 1)

### 5. Collaboration-Friendly
- Nhiều người làm việc cùng lúc
- Git conflicts ít hơn
- Code review dễ hơn (small PRs)
- **Research-friendly**: Mỗi người phụ trách 1-2 demos

### 6. Research Benefits
- **Easy to experiment**: Tạo demo_09_new_idea.py
- **Version control**: demo_01_v1.py, demo_01_v2.py
- **Reusable**: Import demo functions vào research notebooks
- **Documentation**: Mỗi demo có docstring riêng

### Mỗi Demo Dạy:
1. **Basic RSA**: Core algorithm, signatures
2. **Miller-Rabin**: Probabilistic algorithms, primality
3. **CRT**: Optimization techniques, number theory
4. **Pollard Rho**: Cryptanalysis, security
5. **Textbook Padding**: Vulnerabilities, attacks
6. **Wiener**: Advanced attacks, small d problem
7. **Key Size**: Practical security, standards
8. **Properties**: Mathematical foundations

### Kỹ Năng Học Được:
- ✅ RSA algorithm implementation
- ✅ Number theory applications
- ✅ Cryptanalysis techniques
- ✅ Security best practices
- ✅ Performance optimization
- ✅ Web application development
- ✅ API design
- ✅ Research methodology (with Playground modules)

## 📊 Project Status

### ✅ Completed (v1.0)
- [x] 8 comprehensive demos (modular files)
- [x] Clean MVC architecture
- [x] Working Flask API
- [x] Single-page application frontend
- [x] Full CLRS Chapter 31 demonstrations

### 🚧 In Progress (v2.0 - Research Platform)
- [ ] 6 Research Playground modules
- [ ] Data export functionality (JSON/CSV)
- [ ] Interactive parameter exploration
- [ ] Benchmark & visualization tools
- [ ] Academic documentation templates

### 🔮 Future (v3.0+)
- [ ] Advanced cryptanalysis labs
- [ ] Machine learning integration
- [ ] Multi-user research collaboration
- [ ] Citation & reproducibility tools

## 📚 Documentation

- **[README_ARCHITECTURE.md](rsa_tool/README_ARCHITECTURE.md)** - Current architecture details
- **[RESEARCH_ROADMAP.md](rsa_tool/RESEARCH_ROADMAP.md)** - Full research plan with CLRS mapping
- **Code comments** - Inline documentation in all modules

## 🎓 For Academic Use

This tool is designed for:
- **Thesis/Papers**: Generate data, benchmarks, analysis
- **Teaching**: Interactive demonstrations with step-by-step explanations
- **Research**: Playground modules for hypothesis testing
- **Security Analysis**: Real-world attack simulations

**Citation format:**
```
RSA Cryptography Research Tool (2026)
Interactive platform for CLRS Chapter 31: Number-Theoretic Algorithms
GitHub: [repository URL]
```

## 📝 Lưu Ý Quan Trọng

⚠️ **Chỉ dùng cho giáo dục:**
- Đây là textbook RSA (không padding)
- Không dùng trong production
- Real applications cần OAEP/PSS padding

✅ **Best Practices Production:**
- Use `cryptography` library
- Implement proper padding (OAEP)
- Use recommended key sizes (2048+)
- Regular security audits

## 📚 Tài Liệu Tham Khảo

- CLRS Chapter 31: Number-Theoretic Algorithms
- RFC 8017: PKCS #1 v2.2 (RSA Cryptography)
- NIST SP 800-56B: Key Establishment Using RSA
- "Twenty Years of Attacks on the RSA Cryptosystem"

---

**Tác giả:** RSA Tool Development Team  
**Ngày:** January 2026  
**License:** Educational Use Only
