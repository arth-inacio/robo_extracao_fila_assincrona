import os
import json
import pika
from utils.secrets import API_CREDENTIALS


class RabbitEnqueuer:
    def __init__(self, amqp_url: str, queue: str):
        self.amqp_url = amqp_url
        self.queue = queue
        self._user = API_CREDENTIALS["username"]
        self._password = API_CREDENTIALS["password"]

    def enqueue(self, payload: dict) -> None:
        conn = pika.BlockingConnection(pika.URLParameters(self.amqp_url))
        ch = conn.channel()
        ch.queue_declare(queue=self.queue, durable=True)
        ch.basic_publish(
            exchange="",
            routing_key=self.queue,
            body=json.dumps(payload).encode(),
            properties=pika.BasicProperties(
                content_type="application/json",
                delivery_mode=2,
            ),
        )
        conn.close()
        print("Task publicada:", payload)

    def enqueue_multiple_termos(
        self,
        callback_url: str,
        termos: list[str],
        cliente: str = "267511",
        auth_token: str | None = None,
    ) -> None:
        for termo in termos:
            payload = {
                "usuario": self._user,
                "senha": self._password,
                "callback_url": callback_url,
                "termo_busca": termo,
                "cliente": cliente,
            }
            if auth_token:
                payload["auth_token"] = auth_token

            self.enqueue(payload)


AMQP_URL = os.getenv("AMQP_URL", "amqp://app:app123@localhost:5672/app_vhost")
QUEUE = os.getenv("QUEUE", "tarefas.servimed")

if __name__ == "__main__":
    enq = RabbitEnqueuer(AMQP_URL, QUEUE)
    termos = ["PARACETAMOL", "DIPIRONA", "IBUPROFENO"]
    enq.enqueue_multiple_termos(
        callback_url="https://desafio.cotefacil.net",
        termos=termos,
    )