import os
import json
import pika


class RabbitEnqueuer:
    def __init__(self, amqp_url: str, queue: str):
        self.amqp_url = amqp_url
        self.queue = queue

    def enqueue(
        self,
        usuario: str,
        senha: str,
        callback_url: str,
        termo_busca: str = "PARACETAMOL",
        cliente: str = "267511",
        auth_token: str | None = None,
    ) -> None:
        payload = {
            "usuario": usuario,
            "senha": senha,
            "callback_url": callback_url,
            "termo_busca": termo_busca,
            "cliente": cliente,
        }
        if auth_token:
            payload["auth_token"] = auth_token

        # abre conexão, publica e fecha (tudo aqui para ficar simples)
        conn = pika.BlockingConnection(pika.URLParameters(self.amqp_url))
        ch = conn.channel()
        ch.queue_declare(queue=self.queue, durable=True)
        ch.basic_publish(
            exchange="",
            routing_key=self.queue,
            body=json.dumps(payload).encode(),
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=2,  # mensagem persistente
            ),
        )
        conn.close()
        print("Task publicada:", payload)


AMQP_URL = os.getenv("AMQP_URL", "amqp://app:app123@localhost:5672/app_vhost")
QUEUE = os.getenv("QUEUE", "tarefas.servimed")

if __name__ == "__main__":
    enq = RabbitEnqueuer(AMQP_URL, QUEUE)
    enq.enqueue(
        usuario="juliano@farmaprevonline.com.br",
        senha="a007299A",
        callback_url="http://localhost:8000/callback/produtos",
    )
