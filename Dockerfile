# Railway deployment - CPU-only PyTorch (smaller image, faster build)
FROM python:3.10-slim

WORKDIR /app

# Install CPU-only PyTorch first (avoids 2GB+ CUDA deps, reduces build time)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Copy and install other dependencies
COPY requirements-railway.txt .
RUN pip install --no-cache-dir -r requirements-railway.txt

# Copy app files
COPY app.py prompts.json custom.css ./

# Railway sets PORT
ENV PORT=8080
EXPOSE 8080

CMD ["python", "app.py"]
