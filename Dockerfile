# ================================
# BASE IMAGE
# ================================
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=America/Sao_Paulo

WORKDIR /app

# ================================
# DEPENDÊNCIAS DO SISTEMA
# ================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    curl \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# ================================
# INSTALA DEPENDÊNCIAS PYTHON
# ================================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ================================
# COPIA O PROJETO
# ================================
COPY . .

# ================================
# START DO SERVIÇO - PRODUÇÃO
# (Render usa porta aleatória → $PORT)
# ================================
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:${PORT}", "--workers", "3", "--threads", "2"]
