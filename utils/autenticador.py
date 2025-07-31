import requests
from utils.secrets import API_CREDENTIALS
  # carrega variáveis do .env

print("✅ Script iniciado")

def autenticar():
    print("🔑 Autenticando...")
    print("API_USER:", API_CREDENTIALS["username"])
    print("API_PASSWORD:", API_CREDENTIALS["password"])

    payload = {
        "username": API_CREDENTIALS["username"],
        "password": API_CREDENTIALS["password"],
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
