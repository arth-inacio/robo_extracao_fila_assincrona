from rq import Queue
from redis import Redis
from app.worker import job

redis_conn = Redis()
fila = Queue(connection=redis_conn)

tarefa = {
    "usuario": "juliano@farmaprevonline.com.br",
    "senha": "a007299A",
    "callback_url": "https://desafio.cotefacil.net"
}

fila.enqueue(job, **tarefa)
print("Tarefa enfileirada com sucesso!")
