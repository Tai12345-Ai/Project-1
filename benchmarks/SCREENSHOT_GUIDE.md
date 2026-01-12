# 📸 Hướng dẫn Capture Screenshots cho Chapter 4

## 🎯 Mục tiêu
Capture **8 screenshots** cho Chapter 4 thesis (giảm từ 14 → 8 vì dùng video cho demos)

## 📋 Danh sách Screenshots Cần Thiết

### 1. **Web UI Screenshots** (6 ảnh)

#### Screenshot 1: Homepage/Landing Page
- **File name:** `fig_homepage.png`
- **Nội dung:** Trang chủ với menu chính
- **Yêu cầu:** 
  - Hiển thị menu Demos, Playground, API
  - Header với title "RSA Cryptography Tool"
  - Navigation bar rõ ràng

#### Screenshot 2: Demo List View
- **File name:** `fig_demo_list.png`
- **Nội dung:** Danh sách 9 demos với icons và descriptions
- **Yêu cầu:**
  - Hiển thị tất cả 9 demos (01-09)
  - Icons emoji rõ ràng
  - Descriptions ngắn gọn

#### Screenshot 3: Playground Labs Interface
- **File name:** `fig_playground_interface.png`
- **Nội dung:** Giao diện Playground với lab selection
- **Yêu cầu:**
  - Hiển thị 6 labs theo 4 phases
  - Input parameters form
  - Execute button

#### Screenshot 4: JSON Export Example
- **File name:** `fig_json_export.png`
- **Nội dung:** Ví dụ JSON output từ Playground
- **Yêu cầu:**
  - JSON format đẹp (pretty-printed)
  - Hiển thị parameters + results
  - Timestamp và lab info

#### Screenshot 5: Encryption Demo UI
- **File name:** `fig_encryption_ui.png`
- **Nội dung:** Form mã hóa với padding options
- **Yêu cầu:**
  - Input: message, public key (e, n)
  - Padding mode selector (Textbook/OAEP)
  - Output: ciphertext array
  - Encrypt button

#### Screenshot 6: Security Comparison Table
- **File name:** `fig_security_table.png`
- **Nội dung:** Bảng so sánh Textbook vs OAEP vs PSS
- **Yêu cầu:**
  - 3 columns: Textbook, OAEP, PSS
  - Rows: Deterministic, Malleable, Security level
  - ✓/✗ icons rõ ràng

---

### 2. **Charts từ Benchmark** (2 ảnh - tự động generate)

#### Chart 1: CRT Speedup
- **File name:** `fig_crt_speedup.png`
- **Generate bằng:** `python plot_results.py` (sau khi có data)
- **Nội dung:** Bar chart showing speedup 3-4x

#### Chart 2: Padding Overhead
- **File name:** `fig_padding_overhead.png`
- **Generate bằng:** `python plot_results.py`
- **Nội dung:** Line chart comparing Textbook/OAEP/PSS times

---

## 🚀 Hướng dẫn Chi tiết

### Bước 1: Start Web Server

```bash
# Activate virtual environment
source .venv/Scripts/activate  # Windows Git Bash
# hoặc
.venv\Scripts\activate.bat     # Windows CMD

# Start Flask app
cd rsa_tool
python app_simple.py
```

Server sẽ chạy tại: **http://127.0.0.1:5000**

---

### Bước 2: Capture Screenshots

**Tools đề xuất:**
- **Windows:** Snipping Tool (`Win + Shift + S`)
- **Chrome DevTools:** `F12` → Device Toolbar → Responsive mode
- **Firefox:** `Shift + F2` → `screenshot --fullpage`

**Kích thước khuyến nghị:**
- Width: 1200-1400px
- Format: PNG
- Resolution: 96 DPI minimum

**Capture từng màn hình:**

1. **Homepage** → Navigate to `http://127.0.0.1:5000/` → Capture
2. **Demo List** → Click "Demos" menu → Capture toàn bộ list
3. **Playground** → Click "Playground" → Capture interface
4. **JSON Export** → Execute 1 lab → Copy JSON → Capture output
5. **Encryption UI** → Go to Encrypt form → Fill sample data → Capture
6. **Security Table** → (Có thể capture từ README hoặc tạo simple HTML table)

---

### Bước 3: Generate Charts

```bash
# 1. Collect data
python benchmarks/collect_chapter4_data.py
# → Output: chapter4_data.json

# 2. Generate charts
python benchmarks/plot_results.py
# → Output: fig_crt_speedup.png, fig_padding_overhead.png
```

---

### Bước 4: Organize Files

Tạo thư mục `figures/` trong project:

```
Project-1/
├── figures/
│   ├── fig_homepage.png                 # Screenshot 1
│   ├── fig_demo_list.png                # Screenshot 2
│   ├── fig_playground_interface.png     # Screenshot 3
│   ├── fig_json_export.png              # Screenshot 4
│   ├── fig_encryption_ui.png            # Screenshot 5
│   ├── fig_security_table.png           # Screenshot 6
│   ├── fig_crt_speedup.png              # Chart 1 (auto)
│   └── fig_padding_overhead.png         # Chart 2 (auto)
```

---

## 📹 Video Demo (Thay thế Nhiều Screenshots)

**Thay vì capture 4-5 screenshots cho mỗi demo**, chỉ cần:

### Option A: Screen Recording Tool
- **Windows:** Xbox Game Bar (`Win + G`)
- **OBS Studio:** Free, professional
- **ShareX:** Free, có video capture

### Option B: Upload to YouTube/Drive
1. Record màn hình chạy qua 9 demos (5-10 phút)
2. Upload lên YouTube (Unlisted)
3. Lấy link: `https://youtu.be/xxxxx`
4. Trong Chapter 4, thêm:

```latex
\section{Video Demonstration}
Toàn bộ 9 demos được minh họa trong video tổng hợp:
\begin{center}
\url{https://youtu.be/YOUR_VIDEO_ID}
\end{center}

Video bao gồm:
\begin{itemize}
    \item Demo 01-03: Basic RSA, Miller-Rabin, CRT
    \item Demo 04-06: Pollard Rho, Textbook Padding, Wiener Attack
    \item Demo 07-09: Key Size, RSA Properties, Padding Comparison
\end{itemize}
```

---

## ✅ Checklist

- [ ] Start web server (`python app_simple.py`)
- [ ] Capture 6 web UI screenshots
- [ ] Run `collect_chapter4_data.py` để lấy số liệu
- [ ] Run `plot_results.py` để generate 2 charts
- [ ] Organize vào thư mục `figures/`
- [ ] (Optional) Record video demo 9 demos → upload YouTube
- [ ] Copy data từ `chapter4_data.json` vào LaTeX

---

## 🎬 Video Recording Checklist

- [ ] Chuẩn bị script/outline cho 9 demos
- [ ] Clear browser cache/cookies
- [ ] Đóng các tabs không cần thiết
- [ ] Check audio (nếu có narration)
- [ ] Record 1080p, 30fps minimum
- [ ] Upload to YouTube (Unlisted)
- [ ] Copy link vào Chapter 4

---

## 📊 Sau khi có Screenshots + Data

1. **Mở `chapter4_data.json`**
2. **Paste số liệu vào Chapter 4:**
   - Correctness tests: `data['correctness']['tests']`
   - Performance: `data['performance']['modexp']['data']`
   - CRT: `data['performance']['crt']['data']`
   - Padding: `data['performance']['padding']['data']`
3. **Insert figures vào LaTeX:**
   ```latex
   \begin{figure}[h]
   \centering
   \includegraphics[width=0.8\textwidth]{figures/fig_homepage.png}
   \caption{Giao diện trang chủ RSA Tool}
   \label{fig:homepage}
   \end{figure}
   ```

---

## 🔧 Troubleshooting

**Q: Web server không start?**
```bash
# Check port 5000 có bị chiếm không
netstat -ano | findstr :5000

# Thử port khác
python app_simple.py  # Sửa port trong code nếu cần
```

**Q: Charts không generate?**
```bash
# Install dependencies
pip install matplotlib numpy

# Check data file tồn tại
ls chapter4_data.json
```

**Q: Screenshots bị mờ?**
- Zoom browser to 100%
- Capture ở resolution cao hơn
- Export PNG không nén

---

## 📝 Notes

- **KHÔNG CẦN** capture từng demo output chi tiết → Dùng video thay thế
- **CHỈ CẦN** 8 ảnh tổng quan + 1 video link
- Screenshots chỉ để minh họa UI/architecture, không phải results
- Data thực tế lấy từ JSON file, không cần screenshot numbers

