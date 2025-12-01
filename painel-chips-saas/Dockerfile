# ================================
# 🔹 BASE IMAGE
# ================================
FROM python:3.11-slim

# ====== CONFIGS ======
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=10000

WORKDIR /app

# ================================
# 🔹 SISTEMA (dependências do psycopg2)
# ================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ================================
# 🔹 INSTALAR DEPENDÊNCIAS
# ================================
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ================================
# 🔹 COPIAR O PROJETO
# ================================
COPY . .

# ================================
# 🔹 HEALTHCHECK
# ================================
HEALTHCHECK CMD curl --fail http://localhost:${PORT}/healthz || exit 1

# ================================
# 🔹 COMANDO FINAL (usar Gunicorn)
# ================================
CMD gunicorn app:app --bind 0.0.0.0:${PORT} --workers 4 --timeout 120
