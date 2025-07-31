FROM python:3.10-slim

# Cria diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . .

# Instala dependências
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Define comando padrão (pode ser sobrescrito no docker-compose)
CMD ["python", "app/worker.py"]
