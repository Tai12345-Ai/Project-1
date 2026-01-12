# 🚀 RSA Tool Deployment Guide

## 3 Cách Deploy RSA Tool Lên Web Public

---

## 🎯 **Option 1: Render.com (ĐỀ XUẤT - FREE)**

### Tại sao chọn Render?
- ✅ **FREE** tier với 750 giờ/tháng
- ✅ Tự động deploy từ GitHub
- ✅ HTTPS miễn phí
- ✅ Custom domain support
- ✅ Easy setup (5 phút)

### Bước 1: Push Code Lên GitHub

```bash
cd d:/projects/Project-1

# Initialize git nếu chưa có
git init
git add .
git commit -m "Initial commit - RSA Tool"

# Tạo repo mới trên GitHub: https://github.com/new
# Sau đó push:
git remote add origin https://github.com/YOUR_USERNAME/rsa-tool.git
git branch -M main
git push -u origin main
```

### Bước 2: Deploy Trên Render

1. **Đăng ký Render:** https://render.com (dùng GitHub account)

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect GitHub repository: `rsa-tool`
   - Configure:
     - **Name:** `rsa-tool` (hoặc tên bạn muốn)
     - **Region:** Singapore (gần VN nhất)
     - **Branch:** `main`
     - **Root Directory:** (leave blank)
     - **Runtime:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn --chdir rsa_tool --bind 0.0.0.0:$PORT app_simple:app --workers 2 --timeout 120`
   
3. **Environment Variables:** (Optional)
   - `FLASK_ENV` = `production`
   - `PYTHON_VERSION` = `3.13.0`

4. **Create Web Service** → Đợi 3-5 phút

### Bước 3: Lấy Link

Sau khi deploy xong, Render sẽ cho bạn link:

```
https://rsa-tool-xxxxx.onrender.com
```

**GHI CHÚ:** Free tier sẽ sleep sau 15 phút không dùng → lần đầu truy cập chậm (30s), sau đó nhanh.

---

## 🎯 **Option 2: Railway.app (FREE $5 Credit)**

### Ưu điểm Railway
- ✅ $5 credit/tháng miễn phí
- ✅ Deploy cực nhanh
- ✅ Auto HTTPS
- ✅ GitHub integration

### Bước 1: Push Code Lên GitHub (như Option 1)

### Bước 2: Deploy Railway

1. **Đăng ký:** https://railway.app (dùng GitHub)

2. **New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Chọn repository `rsa-tool`

3. **Auto-detect:**
   - Railway tự động detect Python app
   - Tự động chạy theo `Procfile`

4. **Settings:**
   - Trong project → Settings → Generate Domain
   - Copy domain: `rsa-tool.up.railway.app`

### Kết quả:

```
https://rsa-tool.up.railway.app
```

---

## 🎯 **Option 3: Docker + VPS (FULL CONTROL)**

Nếu bạn có VPS (AWS EC2, DigitalOcean, Linode, Azure VM):

### Bước 1: Trên VPS, Install Docker

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt install docker-compose -y
```

### Bước 2: Clone Project

```bash
git clone https://github.com/YOUR_USERNAME/rsa-tool.git
cd rsa-tool
```

### Bước 3: Build và Run

```bash
# Option A: Docker Compose (đề xuất)
docker-compose up -d

# Option B: Docker manual
docker build -t rsa-tool .
docker run -d -p 80:5000 --name rsa-tool-container rsa-tool
```

### Bước 4: Setup Nginx Reverse Proxy (Optional - cho HTTPS)

```bash
sudo apt install nginx certbot python3-certbot-nginx -y

# Tạo nginx config
sudo nano /etc/nginx/sites-available/rsa-tool
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/rsa-tool /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup HTTPS với Let's Encrypt
sudo certbot --nginx -d your-domain.com
```

### Kết quả:

```
https://your-domain.com
```

---

## 📊 **So Sánh 3 Options**

| Feature | Render | Railway | VPS + Docker |
|---------|--------|---------|--------------|
| **Giá** | Free (750h/month) | $5/month credit | ~$5-10/month VPS |
| **Setup Time** | 5 phút | 3 phút | 30 phút |
| **Custom Domain** | ✓ | ✓ | ✓ |
| **HTTPS** | Auto | Auto | Manual (certbot) |
| **Sleep sau 15 min** | ✓ (free tier) | ✗ | ✗ |
| **Performance** | Moderate | Good | Excellent |
| **Control** | Low | Medium | Full |
| **Scaling** | Auto | Auto | Manual |

### Đề xuất:

- **Học tập/Demo thesis:** → **Render** (free, đủ dùng)
- **Production nhỏ:** → **Railway** ($5/month)
- **Full control/Large scale:** → **VPS + Docker**

---

## 🔧 **Troubleshooting**

### Issue 1: Render build timeout

**Fix:** Tăng timeout trong Start Command:
```bash
gunicorn --chdir rsa_tool --bind 0.0.0.0:$PORT app_simple:app --workers 2 --timeout 300
```

### Issue 2: App crash sau khi deploy

**Check logs:**
- Render: Dashboard → Logs tab
- Railway: Dashboard → Deployments → View logs

**Common fixes:**
```bash
# 1. Check Python version
python --version  # Should be 3.13+

# 2. Check dependencies
pip list

# 3. Test locally first
gunicorn --chdir rsa_tool app_simple:app --bind 0.0.0.0:5000
```

### Issue 3: Docker container không start

```bash
# Check logs
docker logs rsa-tool-container

# Debug inside container
docker exec -it rsa-tool-container bash

# Rebuild
docker-compose down
docker-compose up --build -d
```

---

## 📝 **Files Cần Thiết (ĐÃ TẠO)**

Các files sau đã được tạo sẵn trong project:

1. ✅ [requirements.txt](d:/projects/Project-1/requirements.txt) - Python dependencies
2. ✅ [Procfile](d:/projects/Project-1/Procfile) - Start command cho Render/Railway/Heroku
3. ✅ [runtime.txt](d:/projects/Project-1/runtime.txt) - Python version
4. ✅ [Dockerfile](d:/projects/Project-1/Dockerfile) - Docker image build instructions
5. ✅ [docker-compose.yml](d:/projects/Project-1/docker-compose.yml) - Docker orchestration

**KHÔNG CẦN** chỉnh sửa gì, push lên GitHub là xong!

---

## 🎬 **Quick Start - Render (5 Phút)**

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Deploy RSA Tool"
gh repo create rsa-tool --public --source=. --remote=origin --push
# (hoặc tạo repo manually trên GitHub web)

# 2. Đăng ký Render.com

# 3. New Web Service → Connect GitHub repo

# 4. Settings:
#    - Start Command: gunicorn --chdir rsa_tool --bind 0.0.0.0:$PORT app_simple:app --workers 2 --timeout 120
#    - Auto-deploy: YES

# 5. Deploy! 🚀
```

**Sau 3-5 phút, bạn có link:**
```
https://rsa-tool-xxxxx.onrender.com
```

Paste link này vào **Chapter 4 LaTeX**, section Video Demo:

```latex
\textbf{Live Demo:} \url{https://rsa-tool-xxxxx.onrender.com}
```

---

## 🎯 **Dùng Link Này Cho Gì?**

1. **Thesis/Report:** Reviewer có thể truy cập trực tiếp thay vì phải chạy code
2. **Demo cho giảng viên:** Không cần setup environment
3. **Portfolio:** Share với nhà tuyển dụng
4. **Testing:** Bạn bè/classmates có thể test và feedback
5. **Permanent reference:** Link tồn tại lâu dài

---

## 🔒 **Security Notes**

- ⚠️ Đây là **educational tool**, không dùng cho production crypto
- ⚠️ Không lưu sensitive keys trên public deployment
- ⚠️ Rate limiting: Nên thêm nếu deploy public

**Nếu cần thêm security:**

```python
# Thêm vào app_simple.py
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)
```

---

## ✅ **Checklist Deploy**

- [ ] Đã tạo tất cả files (requirements.txt, Procfile, Dockerfile)
- [ ] Đã test locally: `python rsa_tool/app_simple.py`
- [ ] Đã push lên GitHub
- [ ] Đã deploy trên Render/Railway
- [ ] Đã test deployed link
- [ ] Đã paste link vào Chapter 4
- [ ] (Optional) Đã setup custom domain

---

## 📞 **Support**

Nếu gặp vấn đề:
1. Check logs trên Render/Railway
2. Test local bằng Docker: `docker-compose up`
3. Verify dependencies: `pip install -r requirements.txt`

**Ready to deploy!** 🚀
