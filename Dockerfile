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
COPY download_model_build.py ./

# Pre-download model during build (avoids "Fetching 0%" stuck at runtime)
# Railway Variables (HF_TOKEN) are available as build args
ARG HF_TOKEN
ENV HF_TOKEN=${HF_TOKEN}
ENV HF_HUB_ENABLE_HF_TRANSFER=0
RUN python download_model_build.py

# Railway sets PORT
ENV PORT=8080
EXPOSE 8080

ENV HF_HUB_ENABLE_HF_TRANSFER=0

CMD ["python", "app.py"]
