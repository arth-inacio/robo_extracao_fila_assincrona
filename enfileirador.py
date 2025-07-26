from rq import Queue
from redis import Redis
from worker import job

redis_conn = Redis()
fila = Queue(connection=redis_conn)

tarefa = {
    "usuario": "fornecedor_user",
    "senha": "fornecedor_pass",
    "callback_url": "https://desafio.cotefacil.net"
}

fila.enqueue(job, **tarefa)
print("Tarefa enfileirada com sucesso!")
