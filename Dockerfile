# Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Dependências do sistema
RUN apt-get update && apt-get install -y curl git && \
    apt-get clean

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Instala Playwright + Chromium se necessário
RUN pip install playwright && playwright install chromium

CMD ["python", "app/worker.py"]
