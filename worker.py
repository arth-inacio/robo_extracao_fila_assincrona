from dotenv import load_dotenv
from rq import Worker
from redis import Redis
from servimed_scraper import ServimedScraper
from utils.autenticador import autenticar, enviar_callback
import asyncio

load_dotenv()
redis_conn = Redis()

async def processar_scraping(usuario, senha, callback_url):
    scraper = ServimedScraper(usuario, senha)
    await scraper.playwright_start()
    try:
        produtos = await scraper._coletor_cadastros()
    except Exception as e:
        print(f"Erro no scraping: {e}")
        produtos = []
    await scraper.playwright_finish()

    token = autenticar()
    enviar_callback(callback_url, produtos, token)

def job(usuario, senha, callback_url):
    asyncio.run(processar_scraping(usuario, senha, callback_url))

if __name__ == "__main__":
    worker = Worker(["default"], connection=redis_conn)
    worker.work()