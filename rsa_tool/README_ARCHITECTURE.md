# 🏗️ RSA Tool - Tài Liệu Kiến Trúc Hệ Thống

**Tác giả:** Đỗ Văn Tài  
**Mục đích:** Giải thích cấu trúc và thiết kế hệ thống RSA Tool  

---

## 📋 Tổng Quan

RSA Tool là ứng dụng web được xây dựng để minh họa các thuật toán mật mã RSA từ sách **CLRS Chapter 31**. Hệ thống bao gồm 8 demos tương tác và 7 phòng thí nghiệm (labs) nghiên cứu.

### Kiến Trúc Tổng Thể

Hệ thống sử dụng **kiến trúc phân tầng (Layered Architecture)** gồm 4 tầng chính:

```
┌─────────────────────────────────────┐
│   PRESENTATION LAYER (Flask)       │  <- HTTP routes, JSON responses
├─────────────────────────────────────┤
│   SERVICE LAYER (Business Logic)   │  <- RSA operations, validation
├─────────────────────────────────────┤
│   ALGORITHM LAYER (Core Logic)     │  <- Pure math functions
└─────────────────────────────────────┘
```

---

## 📁 Cấu Trúc Thư Mục Chi Tiết

Dự án được tổ chức theo nguyên tắc **Separation of Concerns** (tách biệt trách nhiệm):

```
rsa_tool/
│
├── app_simple.py                    # 🎯 ĐIỂM KHỞI ĐỘNG (Flask Application)
│   ├── Khởi tạo Flask app
│   ├── Định nghĩa các API endpoints (/api/...)
│   ├── Gọi services để xử lý logic
│   └── Trả về JSON responses cho frontend
│
├── services/                        # 🔧 TẦNG LOGIC NGHIỆP VỤ
│   ├── __init__.py                  # Exports các services
│   └── rsa_service.py               # RSAService class - Xử lý RSA
│       ├── generate_keys()          - Sinh cặp khóa (n, e, d)
│       ├── encrypt()                - Mã hóa message
│       ├── decrypt()                - Giải mã (có tùy chọn CRT)
│       ├── sign()                   - Ký số message
│       └── verify()                 - Xác minh chữ ký
│
├── demos/                           # 🎬 8 DEMOS MINH HỌA
│   ├── __init__.py                  # DemoService coordinator - điều phối demos
│   ├── demo_utils.py                # Các hàm dùng chung (imports, helpers)
│   ├── demo_01_basic_rsa.py         ✓ RSA cơ bản (Encrypt/Decrypt)
│   ├── demo_02_miller_rabin.py      ✓ Kiểm tra số nguyên tố
│   ├── demo_03_crt_speed.py         ✓ Tối ưu hóa CRT
│   ├── demo_04_pollard_rho.py       ✓ Phân tích số nguyên
│   ├── demo_05_textbook_padding.py  ✓ Lỗ hổng padding
│   ├── demo_06_wiener_attack.py     ✓ Tấn công Wiener
│   ├── demo_07_key_size_security.py ✓ Phân tích độ an toàn
│   └── demo_08_rsa_properties.py    ✓ Tính chất toán học
│
├── playground/                      # 🔬 7 LABS NGHIÊN CỨU
│   ├── __init__.py                  # PlaygroundService - quản lý labs
│   ├── playground_utils.py          # Utilities dùng chung (benchmark, format)
│   ├── LAB_TEMPLATE.py              # Template chuẩn cho labs mới
│   └── labs/
│       ├── phase1/                  # Phase 1: Lý thuyết số cơ bản
│       │   ├── modular_lab.py       # Số học modulo, CRT
│       │   └── exponentiation_lab.py # Lũy thừa, căn nguyên thủy
│       ├── phase2/                  # Phase 2: Số nguyên tố & RSA
│       │   ├── prime_lab.py         # Kiểm tra nguyên tố
│       │   └── rsa_parameter_lab.py # Tham số RSA
│       ├── phase3/                  # Phase 3: Phân tích mật mã
│       │   ├── factorization_lab.py # Phân tích số nguyên
│       │   └── rsa_attacks_lab.py   # Tấn công RSA
│       └── phase4/                  # Phase 4: Chủ đề nâng cao
│           └── discrete_log_lab.py  # Logarit rời rạc, DH, ElGamal
│
├── templates/
│   └── index.html                   # 📄 GIAO DIỆN WEB (Single Page App)
│       ├── HTML structure
│       ├── Embedded CSS (styling)
│       ├── Embedded JavaScript (logic)
│       └── Gọi API backend (/api/...)
│
└── Algorithms/                      # ⚙️ TẦNG THUẬT TOÁN THUẦN TÚY
    ├── __init__.py
    ├── rsa.py                       # Thuật toán RSA cơ bản
    ├── utilities.py                 # Hàm số học (gcd, modexp, prime...)
    └── pollard_rho.py               # Thuật toán phân tích Pollard Rho
```

---

## 🎯 Giải Thích Chi Tiết Từng Thành Phần

### 1. `app_simple.py` - Tầng Ứng Dụng (Application Layer)

**Trách nhiệm:** Xử lý HTTP requests và responses

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

### 2. `services/rsa_service.py` - Tầng Logic Nghiệp Vụ

**Trách nhiệm:** Xử lý logic RSA (validation, format, error handling)

```python
class RSAService:
    @staticmethod
    def generate_keys(bits=1024, e=65537):
        """Sinh khóa RSA và format kết quả"""
        # Validation
        if bits < 512:
            raise ValueError("Key size too small")
        
        # Gọi algorithm layer
        from Algorithms.rsa import keygen
        keys = keygen(bits, e)
        
        # Format output
        return {
            'public_key': {'n': keys['n'], 'e': keys['e']},
            'private_key': {'d': keys['d']},
            'p': keys['p'],
            'q': keys['q']
        }
```

### 3. `demos/` - Tầng Demos Minh Họa (8 demos độc lập)

**Trách nhiệm:** Minh họa giáo dục - mỗi demo 1 file riêng

**Cấu trúc:**
```
demos/
├── __init__.py                      # DemoService điều phối các demos
├── demo_utils.py                    # Hàm imports và utilities chung
├── demo_01_basic_rsa.py            # 150 dòng - RSA cơ bản
├── demo_02_miller_rabin.py         # 180 dòng - Kiểm tra nguyên tố
├── demo_03_crt_speed.py            # 200 dòng - Tối ưu CRT
├── demo_04_pollard_rho.py          # 130 dòng - Phân tích số
├── demo_05_textbook_padding.py     # 120 dòng - Lỗ hổng padding
├── demo_06_wiener_attack.py        # 90 dòng - Tấn công Wiener
├── demo_07_key_size_security.py    # 130 dòng - Phân tích độ an toàn
└── demo_08_rsa_properties.py       # 150 dòng - Tính chất toán học
```

### 4. `playground/labs/` - Tầng Nghiên Cứu (7 labs)
- ✅ **Dễ bảo trì:** Sửa demo 01 không ảnh hưởng demo 02-08
- ✅ **Dễ mở rộng:** Thêm demo mới chỉ cần tạo file và import
- ✅ **Phù hợp nhóm:** Nhiều người làm việc song song không conflict
- ✅ **Dễ test:** Có thể test từng demo độc lập
- ✅ **Tổ chức tốt:** Mỗi file ~100-200 dòng thay vì 1 file 1100+ dòng

### 4. `playground/labs/` - Tầng Nghiên Cứu (7 labs)

**Trách nhiệm:** Môi trường thử nghiệm và thu thập dữ liệu

**Cấu trúc theo Phase:**
```
labs/
├── phase1/ (Lý thuyết số cơ bản - CLRS 31.1-31.6)
│   ├── modular_lab.py           # Modulo, Extended GCD, CRT
│   └── exponentiation_lab.py    # Lũy thừa, căn nguyên thủy
├── phase2/ (Số nguyên tố & RSA - CLRS 31.7-31.8)
│   ├── prime_lab.py             # Miller-Rabin, Fermat, Trial Division
│   └── rsa_parameter_lab.py     # Tham số RSA, security analysis
├── phase3/ (Phân tích mật mã - CLRS 31.9)
│   ├── factorization_lab.py     # Pollard Rho, Fermat, Trial Division
│   └── rsa_attacks_lab.py       # Wiener, Common Modulus, Broadcast
└── phase4/ (Nâng cao - Beyond CLRS)
    └── discrete_log_lab.py      # DLP, Diffie-Hellman, ElGamal
```

### 5. `templates/index.html` - Giao Diện Web

**Trách nhiệm:** User Interface

**Cấu trúc:**
- HTML: Cấu trúc trang
- CSS (embedded): Styling
- JavaScript (embedded): Gọi API và xử lý events

### 6. `Algorithms/` - Tầng Thuật Toán Thuần Túy

**Trách nhiệm:** Các hàm toán học thuần túy, không phụ thuộc web

**Nội dung:**
- `rsa.py`: Các thuật toán RSA cơ bản
- `utilities.py`: Hàm số học (gcd, modexp, prime...)
- `pollard_rho.py`: Thuật toán phân tích số

---

## 🔄 Luồng Xử Lý Dữ Liệu

### Ví dụ: Sinh khóa RSA

```
1. Browser (index.html)
   └─> POST /api/key/generate {'bits': 1024}

2. Flask (app_simple.py)
   └─> Nhận request
   └─> Gọi RSAService.generate_keys(bits=1024)

3. RSAService (rsa_service.py)
   └─> Validate input
   └─> Gọi Algorithms.rsa.keygen(bits=1024)

4. Algorithms (rsa.py)
   └─> Generate p, q (prime numbers)
   └─> Compute n = p * q
   └─> Compute φ(n) = (p-1)(q-1)
   └─> Compute d (modular inverse)
   └─> Return (public_key, private_key)

5. RSAService
   └─> Format response as JSON
   └─> Return to Flask

6. Flask
   └─> Send JSON response

7. Browser
   └─> Display keys in UI
```

---

## 🎓 Các Nguyên Tắc Thiết Kế Áp Dụng

### 1. Separation of Concerns
- **Routes** (app.py) ← HTTP handling
- **Services** (services/) ← Business logic
- **Demos** (demos/) ← Educational content
- **Templates** (index.html) ← UI

### 2. Maintainability
- Mỗi file có trách nhiệm rõ ràng
- Code dễ đọc, dễ tìm hiểu
- Mỗi file ~100-200 dòng

### 3. Testability
- Test services độc lập (không cần Flask)
- Mock services khi test routes
- Unit test từng layer

### 4. Scalability
- Dễ thêm endpoints mới
- Dễ thêm demos/labs mới
- Có thể tách services thành microservices

### 5. Reusability
- Services dùng được cho CLI, GUI, API khác
- Demos có thể chạy standalone
- Template có thể dùng cho mobile app

---

## 📝 Lưu Ý Quan Trọng
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

---

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

---

## � Tài Liệu Tham Khảo

- CLRS Chapter 31: Number-Theoretic Algorithms
- RFC 8017: PKCS #1 v2.2 (RSA Cryptography)
- NIST SP 800-56B: Key Establishment Using RSA
- "Twenty Years of Attacks on the RSA Cryptosystem"

---

## 👨‍💻 Thông Tin Tác Giả

**Tác giả:** Đỗ Văn Tài  
**Email:** lucdoka1245@gmail.com  
**Mục đích:** Giáo dục và nghiên cứu mật mã học RSA  
**Công nghệ:** Python 3.13, Flask 3.0, CLRS Chapter 31  

**Last Updated:** January 8, 2026  
**Status:** Production Ready - 8 Demos + 7 Labs Complete
