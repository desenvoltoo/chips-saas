FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=America/Sao_Paulo \
    PORT=8000

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ libpq-dev curl tzdata && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expondo a porta 8000 para o Render
EXPOSE 8000

# Executando com Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
