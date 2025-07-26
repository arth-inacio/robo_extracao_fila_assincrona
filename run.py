import asyncio
from dotenv import load_dotenv
import os
from servimed_scraper import ServimedScraper

async def main():
    load_dotenv()  # Carrega as variáveis de ambiente do .env

    usuario = os.getenv("SERVIMED_USUARIO")
    senha = os.getenv("SERVIMED_SENHA")

    if not usuario or not senha:
        raise ValueError("Usuário e/ou senha não definidos no .env")

    scraper = ServimedScraper(usuario, senha)
    await scraper.playwright_start()

    for _ in range(4):
        try:
            produtos = await scraper._coletor_cadastros()
            print(f"✅ {len(produtos)} produtos coletados e salvos com sucesso.")
        except Exception:
            print(f"❌ Erro durante execução, tentando novamente: {_}")
            continue
        break
    await scraper.playwright_finish()

if __name__ == "__main__":
    asyncio.run(main())
