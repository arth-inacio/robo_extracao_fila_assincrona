# arquivo: rodar_scraper.py

import asyncio
from app.coletor.servimed_scraper import ServimedScraper

async def main():
    usuario = "juliano@farmaprevonline.com.br"
    senha = "a007299A"

    scraper = ServimedScraper(usuario, senha)
    await scraper.playwright_start()
    try:
        produtos = await scraper._coletor_cadastros()
        print("Produtos encontrados:")
        for p in produtos:
            print(p)
    except Exception as e:
        print(f"Erro no scraping: {e}")
    finally:
        await scraper.playwright_finish()

asyncio.run(main())