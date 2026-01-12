# Dockerfile for RSA Cryptography Tool
# Build: docker build -t rsa-tool .
# Run: docker run -p 5000:5000 rsa-tool

FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Environment variables
ENV FLASK_APP=rsa_tool/app_simple.py
ENV FLASK_ENV=production
ENV PORT=5000

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000')"

# Run with gunicorn (production server)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "rsa_tool.app_simple:app"]
