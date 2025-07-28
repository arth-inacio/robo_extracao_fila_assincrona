# Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema (Playwright, Redis, etc)
RUN apt-get update && apt-get install -y curl git && \
    pip install --upgrade pip && \
    pip install playwright && \
    playwright install chromium

COPY . .

RUN pip install -r requirements.txt

CMD ["rq", "worker", "default"]
