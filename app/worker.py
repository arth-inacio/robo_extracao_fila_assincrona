import asyncio
import aio_pika
import json
import os
from dotenv import load_dotenv
from app.coletor.servimed_scraper import ServimedScraper
from utils.autenticador import autenticar, enviar_callback

load_dotenv()

async def processar_scraping(usuario, senha, callback_url):
    print("Iniciando o scraper com:", usuario, senha)
    scraper = ServimedScraper(usuario, senha)
    await scraper.playwright_start()
    try:
        print("Rodando _coletor_cadastros()...")
        produtos = await scraper._coletor_cadastros()
    except Exception as e:
        print(f"Erro no scraping: {e}")
        produtos = []
    await scraper.playwright_finish()

    print("Enviando callback...")
    token = autenticar()
    enviar_callback(callback_url, produtos, token)
    print("Callback enviado com sucesso.")

def job(usuario, senha, callback_url):
    print(f"Executando job para {usuario} com callback {callback_url}")

async def callback(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            print("Mensagem recebida bruta:", message.body)
            dados = json.loads(message.body)
            print("Mensagem recebida:", dados)
            await processar_scraping(
                dados["usuario"],
                dados["senha"],
                dados["callback_url"]
            )
        except Exception as e:
            print(f"[ERRO no callback]: {e}")
           

async def main():
    connection = await aio_pika.connect_robust(os.getenv("RABBITMQ_URL"))
    channel = await connection.channel()
    queue = await channel.declare_queue("servimed_queue", durable=True)
    await queue.consume(callback)
    print("Worker iniciado. Aguardando mensagens...")
    await asyncio.Future()  # keep running

if __name__ == "__main__":
    asyncio.run(main())
