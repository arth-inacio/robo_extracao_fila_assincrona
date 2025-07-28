import asyncio
import aio_pika
import json
import os
from dotenv import load_dotenv

load_dotenv()

async def enviar_tarefa(usuario, senha, callback_url):
    connection = await aio_pika.connect_robust(os.getenv("RABBITMQ_URL"))
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue("servimed_queue", durable=True)

        msg = {
            "usuario": usuario,
            "senha": senha,
            "callback_url": callback_url
        }

        await channel.default_exchange.publish(
            aio_pika.Message(body=json.dumps(msg).encode()),
            routing_key=queue.name
        )

if __name__ == "__main__":
    asyncio.run(enviar_tarefa("usuario", "senha", "https://desafio.cotefacil.net"))
