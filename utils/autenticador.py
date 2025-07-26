import requests
import os

def autenticar():
    payload = {
        "username": os.getenv("API_USER"),
        "password": os.getenv("API_PASS"),
        "grant_type": "password"
    }

    response = requests.post("https://desafio.cotefacil.net/oauth/token", data=payload)
    response.raise_for_status()
    return response.json()["access_token"]

def enviar_callback(url, produtos, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(f"{url}/produto", json=produtos, headers=headers)
    response.raise_for_status()
    print("📦 Callback enviado com sucesso.")
