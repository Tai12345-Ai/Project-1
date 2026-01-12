# ��� QUICK DEPLOY - 5 PHÚT

## Bước 1: Commit & Push (1 phút)

```bash
# Trong Git Bash
cd /d/projects/Project-1

# Add all files
git add .

# Commit
git commit -m "Add deployment support - Ready for production"

# Check remote (nếu chưa có thì tạo repo GitHub trước)
git remote -v

# Push to GitHub
git push origin main
# (hoặc: git push origin feature/ui_padding)
```

## Bước 2: Tạo GitHub Repo (nếu chưa có)

Vào: https://github.com/new

- Repository name: `rsa-cryptography-tool`
- Public/Private: Public (để Render free tier)
- Không init README (vì đã có code)

Sau đó:
```bash
git remote add origin https://github.com/YOUR_USERNAME/rsa-cryptography-tool.git
git branch -M main
git push -u origin main
```

## Bước 3: Deploy Render.com (3 phút)

1. **Đăng ký/Login Render:** https://render.com
   - Click "Get Started" hoặc "Sign In"
   - Chọn "GitHub" để login

2. **Connect GitHub:**
   - Authorize Render to access GitHub
   - Select repository: `rsa-cryptography-tool`

3. **Create Web Service:**
   - Click "New +" → "Web Service"
   - Select repo: `rsa-cryptography-tool`
   - **Name:** `rsa-tool` (hoặc tên bạn thích)
   - **Region:** Singapore
   - **Branch:** `main` (hoặc `feature/ui_padding`)
   - **Root Directory:** (leave blank)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** (auto-detect từ Procfile)
     ```
     gunicorn --chdir rsa_tool --bind 0.0.0.0:$PORT app_simple:app --workers 2 --timeout 120
     ```

4. **Free Plan:**
   - Select: **Free** (750 hours/month)
   - Click "Create Web Service"

5. **Đợi Deploy (2-3 phút)**
   - Render sẽ build và deploy
   - Xem logs real-time
   - Khi thấy "Live" → Done!

6. **Copy Link:**
   ```
   https://rsa-tool.onrender.com
   hoặc
   https://rsa-tool-xxxxx.onrender.com
   ```

## Bước 4: Test (1 phút)

Mở browser: `https://rsa-tool-xxxxx.onrender.com`

Test:
- Homepage loads?
- Click "Demos" → Xem list 9 demos
- Click 1 demo → Xem output
- Try encrypt/decrypt

## Bước 5: Paste Link Vào Thesis

Update `latex/chapters/chap4.tex`:

```latex
\section{Live Demo}

RSA Tool đã được deploy công khai tại:

\begin{center}
\Large\url{https://rsa-tool-xxxxx.onrender.com}
\end{center}

Người đọc có thể truy cập trực tiếp để test tool mà không cần cài đặt.
```

## ⚠️ Lưu Ý

**Render Free Tier:**
- Sleep sau 15 phút không dùng
- Lần đầu truy cập chậm (30s wake up)
- Sau khi wake → nhanh bình thường
- 750 giờ/tháng = ~31 ngày (đủ dùng!)

**Nếu muốn NO SLEEP:**
- Upgrade lên Render Starter ($7/month)
- Hoặc dùng Railway ($5/month)

## ��� DONE!

Link để share:
- Thesis: Paste vào Chapter 4
- Email giảng viên: "Tool demo: https://..."
- Portfolio: Add vào CV/GitHub

---

## Troubleshooting

**Q: Build failed?**
- Check logs trong Render dashboard
- Verify `requirements.txt` có đúng không
- Ensure Python 3.13 trong `runtime.txt`

**Q: App crash sau deploy?**
- Check "Logs" tab
- Thường do: thiếu dependencies, wrong start command

**Q: 404 Not Found?**
- Verify Start Command có `--chdir rsa_tool`
- Check `app_simple.py` có trong `rsa_tool/`

**Q: Cannot connect GitHub?**
- Re-authorize Render to access GitHub
- Make repo Public
