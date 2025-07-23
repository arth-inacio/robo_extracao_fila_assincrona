import asyncio
from utils.httpx._async import AsyncHttpx

class ColetordeCadastros:
    usuario: str
    senha: str
    url = "https://pedidoeletronico.servimed.com.br/"

    def __init__(self, usuario: str, senha: str) -> None:
        self.usuario = usuario
        self.senha = senha

        self.session = AsyncHttpx("Coletator").session
        self.session.base_url = self.url

    async def _coletor_cadastros(self):
        await self.session.get(self.url)
        payload = {
            "senha": self.senha,
            "usuario": self.usuario,
        }
        response = await self.session.post("api/usuario/login", json=payload)
        print(response.json())
        return