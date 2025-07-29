# enviar_para_worker.py
import asyncio
import aio_pika
import json

async def enviar_mensagem():
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    channel = await connection.channel()
    
    dados = {
        "usuario": "juliano@farmaprevonline.com.br",
        "senha": "a007299A",
        "callback_url": "http://localhost:8000/callback"  # ou um mock/teste
    }

    mensagem = aio_pika.Message(body=json.dumps(dados).encode())
 
    await channel.default_exchange.publish(
        mensagem,
        routing_key="servimed_queue"
    )

    print("Mensagem enviada para a fila.")
    await connection.close()

asyncio.run(enviar_mensagem())
