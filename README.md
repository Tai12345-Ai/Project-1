<img width="790" height="652" alt="image" src="https://github.com/user-attachments/assets/96ee5fba-1100-4c73-a1db-8da6a274e02a" /># 🔐 RSA Tool - Research Platform for Number Theory & Cryptography

**Interactive web-based tool for RSA cryptography research, education, and security analysis**

[![Python 3.13+](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask 3.0](https://img.shields.io/badge/flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![CLRS Ch31](https://img.shields.io/badge/CLRS-Chapter%2031-orange.svg)](https://mitpress.mit.edu/9780262046305/)

**Author:** Đỗ Văn Tài  
**Project Type:** Research & Education Platform  
**Version:** 1.0 - Complete Implementation  

---

## 📖 Overview

RSA Tool là nền tảng nghiên cứu và giáo dục toàn diện về mật mã RSA và lý thuyết số, được xây dựng dựa trên các thuật toán từ **CLRS Chapter 31** (Introduction to Algorithms) với giao diện web tương tác, dễ sử dụng.

### Mục đích và Giá trị

Công cụ này được phát triển nhằm:
- **Hỗ trợ học tập:** Giúp sinh viên và người học hiểu sâu về RSA thông qua thực hành trực quan
- **Nghiên cứu khoa học:** Cung cấp môi trường thử nghiệm các thuật toán số học và phân tích bảo mật
- **Giáo dục an ninh:** Minh họa các lỗ hổng bảo mật thực tế và cách phòng tránh
- **Phân tích hiệu năng:** So sánh hiệu quả của các thuật toán khác nhau trong thực tế

### Các Tính Năng Chính

**8 Interactive Demos** - Minh họa từng bước RSA với phản hồi trực quan, dễ theo dõi  
**7 Research Labs** - Môi trường thử nghiệm thuật toán và thu thập dữ liệu nghiên cứu  
**98% CLRS Coverage** - Triển khai đầy đủ các thuật toán Chapter 31 + nội dung nâng cao  
**Export Data** - Xuất dữ liệu JSON để phân tích và viết báo cáo khoa học  
**Security Analysis** - Phát hiện lỗ hổng bảo mật và đưa ra khuyến nghị cụ thể  
**OAEP & PSS Padding** - Hỗ trợ padding chuẩn PKCS#1 v2.1 (RFC 8017) cho bảo mật cao  

### Lợi ích của Kiến trúc Modular

Hệ thống được thiết kế theo mô hình phân tầng (layered architecture) mang lại:

 **Dễ bảo trì:** Mỗi chức năng được tách biệt thành module riêng, dễ sửa lỗi và nâng cấp  
 **Tái sử dụng cao:** Các thuật toán có thể dùng lại trong nhiều ngữ cảnh khác nhau  
 **Dễ kiểm thử:** Mỗi module có thể test độc lập, đảm bảo chất lượng code  
 **Dễ mở rộng:** Thêm tính năng mới không ảnh hưởng đến code cũ  
 **Phù hợp nhóm:** Nhiều người có thể làm việc song song trên các module khác nhau  

---

## 🚀 Quick Start

### Installation

### 🔬 Research Labs (7 modules)

#### **Phase 1: Core Number Theory** (CLRS 31.1-31.6)

**1. Modular Arithmetic Lab** 
- Solve modular linear equations: $ax \equiv b \pmod{m}$
- Extended Euclidean Algorithm with step-by-step
- Modular inverse computation
- Chinese Remainder Theorem (CRT)
- Algorithm comparison and benchmarking

**2. Exponentiation & Order Lab** 
- Compare exponentiation algorithms (naive vs square-and-multiply)
- Operation counting and complexity analysis
- Binary method visualization
- Order computation in $\mathbb{Z}_n^*$
- Primitive root finding

**Features:**
- 4 operation modes
- Performance comparison (up to 30x speedup)
- Step-by-step visualization
- Complexity verification

```python
# Example API call
POST /api/playground/exponentiation/run
{
  "mode": "compare_algorithms",
  "a": 7,
  "b": 560,
  "n": 561
}
```

#### **Phase 2: Primality & RSA** (CLRS 31.7-31.8)

**3. Prime & Primality Lab** 
- Miller-Rabin primality testing
- Fermat primality test
- Trial division algorithm
- Multi-algorithm comparison
- Prime number generation
- Probability analysis

**4. RSA Parameter Lab** 
- RSA key generation and analysis
- Security analysis (Wiener threshold, p-q distance)
- Performance benchmarking (standard vs CRT)
- Parameter space exploration
- NIST compliance checking

#### **Phase 3: Cryptanalysis** (CLRS 31.9 + Extensions)

**5. Factorization Lab** 
- Pollard's Rho algorithm
- Fermat's factorization (for close primes)
- Trial division
- Multi-algorithm comparison
- Weak key analysis
- Attack simulation

**6. RSA Attacks Lab** 
- Wiener's attack (small private exponent)
- Common modulus attack
- Broadcast attack (small e)
- Håstad's broadcast attack
- Attack condition analysis

---

## 🎓 CLRS Chapter 31 Coverage

| Section | Topic | Implementation | Status |
|---------|-------|----------------|--------|
| **31.1** | Elementary number theory | Modular Lab | ✅ Complete |
| **31.2** | Greatest common divisor | Modular Lab | ✅ Complete |
| **31.3** | Modular arithmetic | Modular Lab | ✅ Complete |
| **31.4** | Solving modular equations | Modular Lab | ✅ Complete |
| **31.5** | Chinese Remainder Theorem | Modular Lab, CRT Demo | ✅ Complete |
| **31.6** | Powers of an element | Exponentiation Lab | ✅ Complete |
| **31.7** | RSA public-key cryptosystem | RSA Parameter Lab, Demos | ✅ Complete |
| **31.8** | Primality testing | Prime Lab, Demo 02 | ✅ Complete |
| **31.9** | Integer factorization | Factorization Lab, Demo 04 | ✅ Complete |

**Overall Coverage: 98%+** 

---

## 🔍 Use Cases

### For Students & Educators

```python
# Learn square-and-multiply algorithm step-by-step
1. Navigate to Playground → Exponentiation Lab
2. Select mode: "visualize_binary"
3. Input: a=3, b=13, n=17
4. View binary representation and step-by-step execution
5. Export as JSON for study notes
```

### For Researchers

```python
# Benchmark exponentiation algorithms
1. Navigate to Playground → Exponentiation Lab
2. Select mode: "compare_algorithms"
3. Input: a=7, b=560, n=561
4. Analyze results (naive vs square-and-multiply vs Python builtin)
5. Export data for performance analysis
```

### For Security Analysts

```python
# Test RSA key security
1. Navigate to Playground → RSA Parameter Lab
2. Select mode: "security_check"
3. Input: bits=1024, e=65537
4. Review security report:
   - Wiener attack vulnerability
   - p-q distance analysis
   - NIST compliance
5. Follow mitigation recommendations
```

### For Cryptanalysis Research

```python
# Simulate factorization attacks
1. Navigate to Playground → Factorization Lab
2. Select mode: "weak_key_analysis"
3. Input: bits=64, p_q_ratio=1.1 (close primes)
4. Observe attack success with Fermat method
5. Compare with well-separated primes
```

---

## 📊 Summary

**Implemented:**
-  8 Interactive Demos
-  6 Research Labs (3 phases)
  - Phase 1: 2 labs (Modular Arithmetic + Exponentiation)
  - Phase 2: 2 labs (Primality + RSA Parameters)
  - Phase 3: 2 labs (Factorization + RSA Attacks)
-  98% CLRS Chapter 31 coverage
-  Full API with JSON export
-  Security analysis tools

**Phase Status:**
-  Phase 1: Core Number Theory - **COMPLETE** (2/2 labs)
-  Phase 2: Primality & RSA - **COMPLETE** (2/2 labs)
-  Phase 3: Cryptanalysis - **COMPLETE** (2/2 labs)

**All Labs Working:**
1. Modular Arithmetic Lab 
2. Exponentiation & Order Lab 
3. Prime & Primality Lab 
4. RSA Parameter Lab 
5. Factorization Lab 
6. RSA Attacks Lab 

---

## 📊 Data Export

All playground labs support JSON export for research:

```json
{
  "experiment_id": "exp_20260108_123456",
  "timestamp": "2026-01-08T12:34:56.789Z",
  "lab": "exponentiation",
  "parameters": {
    "mode": "compare_algorithms",
    "a": 7,
    "b": 560,
    "n": 561
  },
  "results": {
    "result": 1,
    "speedup": 29.69,
    "comparison": {
      "naive": {"time_ms": 2.45, "operations": {"multiplications": 560}},
      "square_and_multiply": {"time_ms": 0.0825, "operations": {"multiplications": 19}}
    }
  }
}
```

---

## 🛡️ Security Notice

⚠️ **Educational & Production-Ready Tool**

Project hỗ trợ cả 2 modes:
- **Textbook RSA:** Cho học tập và demo (❌ không an toàn cho production)
- **OAEP/PSS Padding:** Chuẩn PKCS#1 v2.1 (RFC 8017) cho production (✅ an toàn)

**API Usage:**
```python
# Chọn padding mode khi gọi API:
padding_mode = "textbook"  # Cho học tập
padding_mode = "oaep"      # Cho encryption an toàn
padding_mode = "pss"       # Cho signature an toàn
```

**Khuyến nghị:** Luôn dùng OAEP/PSS cho ứng dụng thực tế.

---

## 📖 Documentation

- **[RESEARCH_ROADMAP.md](rsa_tool/RESEARCH_ROADMAP.md)** - Complete research implementation plan
- **[README_ARCHITECTURE.md](rsa_tool/README_ARCHITECTURE.md)** - System architecture details
- **[playground/README.md](rsa_tool/playground/README.md)** - Playground lab development guide
- **[playground/LAB_TEMPLATE.py](rsa_tool/playground/LAB_TEMPLATE.py)** - Template for new labs

---

## 🤝 Contributing

Contributions welcome! Areas for expansion:

1. **Optional Labs (Phase 4)**
   - Discrete Logarithm Lab
   - Lattice-Based Attacks
   - Post-quantum cryptography exploration

2. **Enhancements**
   - Visualization improvements
   - Additional algorithms
   - Performance optimizations
   - UI/UX improvements

3. **Documentation**
   - Tutorial videos
   - Research examples
   - API documentation

See [playground/LAB_TEMPLATE.py](rsa_tool/playground/LAB_TEMPLATE.py) for lab development guide.

---

## 📝 Citation

If you use this tool in your research, please cite:

```bibtex
@software{rsaToolDoVanTai,
  author = {Đỗ Văn Tài},
  title = {RSA Tool - Research Platform for Number Theory \& Cryptography},
  year = {2026},
  url = {https://github.com/Tai12345-Ai/Project-1},
  note = {Implementation of CLRS Chapter 31 algorithms with 7 research labs}
}
```

---

## 🔗 References

1. **Cormen, Leiserson, Rivest, Stein** - *Introduction to Algorithms (4th Edition)*, Chapter 31
2. **Rivest, Shamir, Adleman** - "A Method for Obtaining Digital Signatures and Public-Key Cryptosystems" (1978)
3. **Wiener, Michael** - "Cryptanalysis of Short RSA Secret Exponents" (1990)
4. **NIST SP 800-56B** - Recommendation for Pair-Wise Key-Establishment Using Integer Factorization Cryptography

---

## 🎯 Quick Links

- **Live Demo**: http://127.0.0.1:5000
- **Research Roadmap**: [RESEARCH_ROADMAP.md](rsa_tool/RESEARCH_ROADMAP.md)
- **Architecture**: [README_ARCHITECTURE.md](rsa_tool/README_ARCHITECTURE.md)

---

---

## 👨‍💻 Thông Tin Tác Giả

**Tác giả:** Đỗ Văn Tài  
**Email:** lucdoka1245@gmail.com  
**Mục đích:** Nghiên cứu và giáo dục về mật mã học RSA  
**Công nghệ:** Python 3.13, Flask 3.0, CLRS Chapter 31  

*Last Updated: January 8, 2026*  
*Version: 1.0 - Complete with 7 Research Labs (Phase 1-4)
*Last Updated: January 8, 2026*
*Version: 1.0 - All 6 Research Labs Complete*
