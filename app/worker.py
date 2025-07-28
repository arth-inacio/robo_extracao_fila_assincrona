import asyncio
import aio_pika
import json
import os
from dotenv import load_dotenv
from app.coletor.servimed_scraper import ServimedScraper
from utils.autenticador import autenticar, enviar_callback

load_dotenv()

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

async def callback(message: aio_pika.IncomingMessage):
    async with message.process():
        dados = json.loads(message.body)
        print("Mensagem recebida:", dados)
        await processar_scraping(
            dados["usuario"],
            dados["senha"],
            dados["callback_url"]
        )

async def main():
    connection = await aio_pika.connect_robust(os.getenv("RABBITMQ_URL"))
    channel = await connection.channel()
    queue = await channel.declare_queue("servimed_queue", durable=True)
    await queue.consume(callback)
    print("Worker iniciado. Aguardando mensagens...")
    await asyncio.Future()  # keep running

if __name__ == "__main__":
    asyncio.run(main())
