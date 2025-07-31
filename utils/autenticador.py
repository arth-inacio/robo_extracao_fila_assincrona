import os
import requests
from dotenv import load_dotenv

load_dotenv()  # carrega variáveis do .env

print("✅ Script iniciado")

def autenticar():
    print("🔑 Autenticando...")
    print("API_USER:", os.getenv("API_USER"))
    print("API_PASS:", os.getenv("API_PASS"))

    payload = {
        "username": os.getenv("API_USER"),
        "password": os.getenv("API_PASS"),
        "grant_type": "password"
    }

    response = requests.post("https://desafio.cotefacil.net/oauth/token", data=payload)
    print("📡 Status:", response.status_code)
    print("📥 Resposta:", response.text)
    response.raise_for_status()

    token = response.json()["access_token"]
    print("✅ Token recebido:", token)
    return token


if __name__ == "__main__":
    autenticar()
