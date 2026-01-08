# 🔬 RSA Tool - Roadmap Nghiên Cứu (Research Roadmap)

## 📘 Dựa trên CLRS Chapter 31: Number-Theoretic Algorithms

Document này mô tả **đầy đủ** các hướng nghiên cứu và playground modules để bao quát toàn bộ Chương 31.

---

## 🎯 Mục tiêu tổng quan

Biến RSA Tool từ **demo tool** thành **research platform** cho:
- Nghiên cứu thuật toán số học
- Phân tích bảo mật RSA
- Benchmark & optimization
- Thu thập dữ liệu cho báo cáo khoa học

---

## 📊 Mapping CLRS Chapter 31 → Research Modules

### **Phase 1: Core Number Theory (CLRS 31.1-31.5)** ✅ Ưu tiên cao

#### 1️⃣ **Modular Arithmetic Lab**
**Nội dung CLRS:**
- 31.1 Elementary number-theoretic notions
- 31.2 Greatest common divisor (Euclid)
- 31.3 Modular arithmetic
- 31.4 Solving modular linear equations

**Chức năng nghiên cứu:**
- ✅ Giải phương trình: $ax \equiv b \pmod{m}$
- ✅ Extended Euclidean Algorithm với step-by-step
- ✅ Tìm nghịch đảo modulo: $a^{-1} \bmod m$
- ✅ Chinese Remainder Theorem (CRT) - giải hệ đồng dư
- 🆕 Visualize số nghiệm trên number line
- 🆕 So sánh hiệu năng Euclid vs Binary GCD

**Output nghiên cứu:**
- Step-by-step solution
- Kiểm tra điều kiện tồn tại nghiệm
- Benchmark thời gian theo input size
- Export data (JSON/CSV)

---

#### 2️⃣ **Exponentiation & Order Lab** 🆕 Cần thiết
**Nội dung CLRS:**
- 31.6 Powers of an element (modular exponentiation)
- Order of element, primitive roots
- Repeated squaring algorithm

**Chức năng nghiên cứu:**
- ✅ So sánh thuật toán mũ:
  - Naive: $a^b \bmod n$ (b phép nhân)
  - Square-and-multiply (binary method)
  - Montgomery multiplication
- ✅ Đếm số phép toán (multiply, mod) cho từng method
- ✅ Visualize binary representation của exponent
- ✅ Tính order của phần tử trong $\mathbb{Z}_n^*$
- ✅ Tìm primitive roots modulo n
- 🆕 Benchmark theo exponent size và modulus size

**Output nghiên cứu:**
- Bảng so sánh số phép toán
- Graph: time vs exponent bits
- Phân tích độ phức tạp thực tế
- Data export cho analysis

**Ý nghĩa:** Đây là "engine" đằng sau RSA encrypt/decrypt, Miller-Rabin.

---

### **Phase 2: Primality & RSA (CLRS 31.7-31.8)** ✅ Đã có, cần mở rộng

#### 3️⃣ **Prime & Primality Lab** ✅ Đã có cơ bản
**Nội dung CLRS:**
- 31.8 Primality testing
- Miller-Rabin algorithm
- Prime density & distribution

**Chức năng hiện tại:**
- ✅ Miller-Rabin test với configurable rounds
- ✅ Prime generation benchmark
- ✅ Xác suất sai phân tích

**Cần mở rộng:**
- 🆕 So sánh nhiều primality tests:
  - Trial division
  - Miller-Rabin
  - Fermat test
  - Solovay-Strassen
  - (Optional) AKS deterministic test cho số nhỏ
- 🆕 Phân tích phân bố prime:
  - Prime counting function $\pi(x)$
  - Prime gaps statistics
  - Twin primes, Sophie Germain primes
- 🆕 Carmichael numbers testing
- 🆕 Prime generation strategies comparison

**Output nghiên cứu:**
- Multi-algorithm benchmark table
- Distribution graphs
- Gap analysis data
- Export cho statistical analysis

---

#### 4️⃣ **RSA Parameter Lab** ✅ Đã có cơ bản
**Nội dung CLRS:**
- 31.7 RSA public-key cryptosystem
- Key generation, encryption, decryption
- Security parameters

**Chức năng hiện tại:**
- ✅ Configurable e, key size
- ✅ CRT optimization benchmark
- ✅ Basic security checks

**Cần mở rộng:**
- 🆕 Security analysis chi tiết:
  - Check d size (Wiener threshold)
  - Check p-q distance (Fermat risk)
  - Check e coprimality
  - Multi-prime RSA research
- 🆕 Parameter space exploration:
  - Matrix: key_size × e × p_q_ratio
  - Heatmap: security score
  - Pareto frontier: security vs performance
- 🆕 Real-world configurations:
  - PKCS#1 compliance check
  - NIST recommendations adherence
- 🆕 Hybrid schemes research (RSA + AES)

**Output nghiên cứu:**
- Comprehensive security report
- Parameter recommendation engine
- Multi-dimensional benchmark data
- Compliance checklist

---

### **Phase 3: Cryptanalysis (CLRS 31.9 + Extensions)** 🆕 Quan trọng

#### 5️⃣ **Factorization Lab** 🆕 Cần thiết
**Nội dung CLRS:**
- 31.9 Integer factorization
- Pollard's rho algorithm
- Security implications

**Chức năng nghiên cứu:**
- ✅ Pollard Rho (đã có demo cơ bản)
- 🆕 Nhiều thuật toán factorization:
  - Trial division
  - Pollard Rho (tối ưu hóa)
  - Pollard p-1
  - Fermat factorization (cho p≈q)
  - Williams p+1
  - (Optional) Quadratic Sieve simulation nhỏ
- 🆕 Benchmark theo:
  - Bit size (40, 64, 96, 128, 160, ...)
  - p-q distance
  - Số iterations
- 🆕 Attack scenario simulation:
  - Weak key detection
  - Time-to-factor estimation
  - Success rate analysis

**Output nghiên cứu:**
- Algorithm comparison table
- Time complexity verification
- Attack feasibility matrix
- Recommendations cho key generation

**Ý nghĩa:** Hiểu "tại sao RSA an toàn" và "khi nào không an toàn".

---

#### 6️⃣ **RSA Attacks Lab** 🆕 Mở rộng security
**Nội dung:** Các attacks ngoài factorization

**Chức năng nghiên cứu:**
- 🆕 Wiener's attack (small d):
  - Continued fraction implementation
  - Threshold analysis
  - Success rate vs d size
- 🆕 Common modulus attack
- 🆕 Broadcast attack (small e, same message)
- 🆕 Håstad's attack
- 🆕 Timing attacks simulation
- 🆕 Padding oracle (Bleichenbacher)
- 🆕 Fault attacks (CRT-based)

**Output nghiên cứu:**
- Attack success matrix
- Parameter vulnerability map
- Mitigation strategies
- Real-world case studies

---

### **Phase 4: Advanced Topics (Optional)** 🔮 Mở rộng

#### 7️⃣ **Discrete Logarithm Lab** 🆕 Nice-to-have
**Nội dung:** Discrete log problem (liên quan Diffie-Hellman)

**Chức năng nghiên cứu:**
- 🆕 Discrete log algorithms:
  - Baby-step Giant-step
  - Pollard's rho for DLP
  - Pohlig-Hellman
- 🆕 DLP vs Factorization comparison
- 🆕 Diffie-Hellman key exchange demo
- 🆕 ElGamal encryption

**Output nghiên cứu:**
- Algorithm complexity verification
- Security comparison with RSA
- Post-quantum implications

---

#### 8️⃣ **Lattice-Based Attacks Lab** 🔮 Advanced
**Nội dung:** Modern attacks sử dụng lattice reduction

**Chức năng nghiên cứu:**
- 🆕 Coppersmith's attack
- 🆕 LLL algorithm visualization
- 🆕 Small plaintext/ciphertext attacks

---

## 📐 Implementation Architecture

```
rsa_tool/
├── playground/                      # 🆕 Research Modules
│   ├── __init__.py
│   ├── playground_utils.py         # Shared utilities
│   │
│   ├── modular_lab.py              # ✅ Phase 1.1
│   ├── exponentiation_lab.py       # 🆕 Phase 1.2 (NEW!)
│   │
│   ├── prime_lab.py                # ✅ Phase 2.1 (expand)
│   ├── rsa_parameter_lab.py        # ✅ Phase 2.2 (expand)
│   │
│   ├── factorization_lab.py        # 🆕 Phase 3.1 (NEW!)
│   ├── rsa_attacks_lab.py          # 🆕 Phase 3.2 (NEW!)
│   │
│   └── discrete_log_lab.py         # 🔮 Phase 4.1 (optional)
│
├── demos/                          # ✅ Existing demos
├── services/                       # ✅ Existing services
└── templates/
    └── index.html                  # 🆕 Add "Playground" tab
```

---

## 🎯 Priority & Timeline

### **Must Have (Bao quát core Ch31)**
1. ✅ Modular Arithmetic Lab - **Week 1**
2. 🆕 Exponentiation & Order Lab - **Week 2**
3. ✅ Prime & Primality Lab (expand) - **Week 3**
4. 🆕 Factorization Lab - **Week 4**
5. ✅ RSA Parameter Lab (expand) - **Week 5**

### **Should Have (Security research)**
6. 🆕 RSA Attacks Lab - **Week 6**

### **Nice to Have (Advanced topics)**
7. 🔮 Discrete Logarithm Lab - **Week 7+**
8. 🔮 Lattice-Based Attacks - **Future**

---

## 📊 Research Output Standards

Mỗi lab phải cung cấp:

### 1. Interactive Interface
- Real-time parameter adjustment
- Live result updates
- Visual feedback (graphs, tables)

### 2. Data Export
```json
{
  "experiment_id": "exp_20260108_001",
  "timestamp": "2026-01-08T00:00:00Z",
  "lab": "modular_arithmetic",
  "parameters": {
    "a": 5,
    "b": 3,
    "m": 7
  },
  "results": {
    "solution": 2,
    "steps": [...],
    "time_ms": 0.42
  },
  "metadata": {
    "python_version": "3.13.1",
    "tool_version": "1.0.0"
  }
}
```

### 3. Reproducibility
- Seed control cho random algorithms
- Version tracking
- Parameter logging

### 4. Visualization
- Graphs (matplotlib/plotly export)
- Tables (CSV/LaTeX export)
- Step-by-step animation

---

## 🎓 Academic Use Cases

### For Thesis/Papers:
```
1. Generate datasets → statistical analysis
2. Benchmark comparisons → tables/figures
3. Security evaluation → vulnerability assessment
4. Algorithm complexity → empirical verification
```

### For Teaching:
```
1. Interactive demonstrations
2. Step-by-step algorithm visualization
3. Parameter exploration
4. Hands-on experiments
```

### For Security Research:
```
1. Attack scenario simulation
2. Vulnerability discovery
3. Mitigation testing
4. Real-world configuration analysis
```

---

## 🚀 Getting Started

### MVP Implementation 
Bắt đầu với **2 labs** để chứng minh concept:

1. **Modular Arithmetic Lab** (dễ, cơ bản)
   - Giải $ax \equiv b \pmod{m}$
   - Extended Euclidean
   - Export JSON

2. **Exponentiation Lab** (quan trọng)
   - Square-and-multiply visualization
   - Operation counting
   - Benchmark

→ **Mục tiêu:** Có 2 labs chạy được, có UI đơn giản, export data được.

### Full Implementation 
Hoàn thiện 6 labs "Must Have" và "Should Have".

### Advanced 
Thêm optional modules dựa trên feedback và nhu cầu nghiên cứu.

---

## 📝 Documentation Requirements

Mỗi lab cần có:

1. **Algorithm Description** (CLRS section reference)
2. **Parameter Guide** (what to adjust, valid ranges)
3. **Interpretation Guide** (how to read results)
4. **Research Examples** (sample experiments)
5. **Data Export Format** (JSON schema)
6. **Citation Information** (how to cite in papers)

---

## ✅ Success Metrics

Project được coi là "bao quát Ch31" khi:

- ✅ Cover 80%+ nội dung CLRS 31.1-31.9
- ✅ Có ít nhất 6 playground labs hoạt động
- ✅ Mỗi lab có data export
- ✅ Có ít nhất 3 research use case examples
- ✅ Documentation đầy đủ
- ✅ Có thể reproduce experiments

---

## 🎯 Next Actions

1. **Tạo structure folders** cho playground/
2. **Implement MVP** (2 labs đầu)
3. **Design UI** cho Playground tab
4. **Test & iterate**
5. **Expand** theo priority list

---

**Version:** 1.0  
**Date:** January 8, 2026  
**Status:** 📋 Planning → 🚧 Implementation Ready
