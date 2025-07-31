# app/worker_rabbit.py
import os
import json
import logging
from typing import Any, Dict, Optional, List
import pika
import requests
import asyncio
from utils.autenticador import autenticar
from app.coletor.servimed_scraper import ServimedScraper

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

class CallbackClient:
    def __init__(self, base_url: str, token: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def send_products(self, products: List[Dict[str, Any]]) -> None:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        r = requests.post(f"{self.base_url}", json=products, headers=headers, timeout=60)
        r.raise_for_status()
        logging.info("Callback OK: status=%s", r.status_code)

class RabbitWorker:
    def __init__(self, amqp_url: str, queue: str, prefetch: int = 1):
        self.amqp_url = amqp_url
        self.queue = queue
        self.prefetch = prefetch
        self._conn: Optional[pika.BlockingConnection] = None
        self._ch: Optional[pika.adapters.blocking_connection.BlockingChannel] = None

    def start(self) -> None:
        logging.info("Conectando ao RabbitMQ...")
        params = pika.URLParameters(self.amqp_url)
        self._conn = pika.BlockingConnection(params)
        self._ch = self._conn.channel()
        self._ch.queue_declare(queue=self.queue, durable=True)
        self._ch.basic_qos(prefetch_count=self.prefetch)
        self._ch.basic_consume(queue=self.queue, on_message_callback=self._on_message)
        logging.info("Consumindo fila '%s' (Ctrl+C para sair)...", self.queue)

        try:
            self._ch.start_consuming()
        except KeyboardInterrupt:
            logging.info("Interrompido pelo usuário")
            self._ch.stop_consuming()
        finally:

            try:
                if self._ch and self._ch.is_open:
                    self._ch.close()
            finally:
                if self._conn and self._conn.is_open:
                    self._conn.close()
            logging.info("Conexão encerrada.")

    def _on_message(self, ch, method, _, body: bytes) -> None:
        auth_token = autenticar()
        try:
            payload = json.loads(body.decode())
            logging.info("Payload recebido: %s", payload)

            self._validate_payload(payload)

            # 1) Rodar seu scraper (async) → lista de produtos
            logging.info("Iniciando scraper para termo: %s", payload.get("termo_busca"))
            produtos = asyncio.run(self._run_scraper(payload))
            logging.info("Produtos coletados: %s", produtos)

            # 2) Disparar callback com os produtos
            callback = CallbackClient(
                base_url=payload["callback_url"],
                token=auth_token,
            )
            callback.send_products(produtos)

            ch.basic_ack(delivery_tag=method.delivery_tag)
            logging.info("OK - mensagem processada.")

        except Exception as e:

            logging.exception("Erro ao processar: %s", e)
            # simples: não re-enfileirar para evitar loop infinito
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    async def _run_scraper(self, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        scraper = ServimedScraper()
        termo = payload.get("termo_busca", "PARACETAMOL")
        cliente = payload.get("cliente", "267511")
        return await scraper.collect_products(termo_busca=termo, cliente=cliente)

    @staticmethod
    def _validate_payload(payload: Dict[str, Any]) -> None:
        required = ["usuario", "senha", "callback_url"]
        missing = [k for k in required if k not in payload]
        if missing:
            raise ValueError(f"Campos obrigatórios ausentes: {missing}")

if __name__ == "__main__":
    AMQP_URL = os.getenv("AMQP_URL", "amqp://app:app123@localhost:5672/app_vhost")
    QUEUE = os.getenv("QUEUE", "tarefas.servimed")
    PREFETCH = int(os.getenv("PREFETCH", "1"))
    RabbitWorker(AMQP_URL, QUEUE, PREFETCH).start()
