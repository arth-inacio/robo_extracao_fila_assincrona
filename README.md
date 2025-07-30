<h1>🚀 Desafio Python - Robô de Extração com Fila Assíncrona</h1>

<p>Este projeto é parte de um desafio técnico que simula a construção de um robô de scraping com <strong>workflow assíncrono</strong>, uso de <strong>filas</strong>, <strong>callback com autenticação</strong> e consumo de API via <strong>FastAPI</strong>. O sistema foi pensado para funcionar de forma desacoplada e escalável, simulando um ambiente de produção real.</p>

<hr>

<h2>🧱 Arquitetura Geral</h2>

<p><strong>Fluxo simplificado:</strong></p>

<pre>
Client (API) → RabbitMQ (Queue) → Worker (Scraping) → Callback (FastAPI)
</pre>

<hr>

<h2>⚙️ Funcionalidades</h2>
<ul>
  <li>✅ Adicionar tarefas de scraping a uma fila (Rabbitmq)</li>
  <li>✅ Consumir fila com worker assíncrono (Playwright + asyncio)</li>
  <li>✅ Enviar resultado do scraping via callback autenticado</li>
  <li>✅ Simular cenário real com autenticação, fila e retorno de resultado</li>
</ul>

<hr>

<h2>🧪 Tecnologias Utilizadas</h2>
<ul>
  <li><strong>Python 3.11+</strong></li>
  <li><strong>FastAPI</strong> – API moderna e assíncrona</li>
  <li><strong>RabbitMQ</strong> – Gerenciamento de fila</li>
  <li><strong>Playwright</strong> – Robô de scraping assíncrono</li>
  <li><strong>HTTPx & Requests</strong> – Requisições HTTP com suporte assíncrono</li>
  <li><strong>Uvicorn</strong> – Servidor ASGI para FastAPI</li>
  <li><strong>Pydantic</strong> – Validação de dados</li>
</ul>

<hr>

<h2>🗂️ Estrutura do Projeto</h2>

<pre>
desafio-python/
├── app/
│ ├── worker.py # Worker que executa scraping via fila
│ ├── enfileirador.py # Envia tarefas de scraping para a fila
│ ├── coletor/
│ │ └── servimed_scraper.py # Scraper Playwright
│ ├── utils/
│ │ ├── autenticador.py # Autenticação e callback
│ │ └── storage.py # Salva JSON local
│ └── .env # Variáveis de ambiente
├── Dockerfile # Docker do projeto
├── docker-compose.yml # Orquestra rabbitmq + app
├── requirements.txt # Dependências
└── README.md
</pre>

<hr>

<h2>🚀 Como Executar o Projeto</h2>

<h3>1. Clone o repositório</h3>
<pre><code>
git clone https://github.com/arth-inacio/desafio-python.git
cd desafio-python
</code></pre>

<h3>2. Crie e ative um ambiente virtual</h3>
<pre><code>
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate        # Windows
</code></pre>

<h3>3. Instale as dependências</h3>
<pre><code>
pip install -r requirements.txt
</code></pre>

<h3>4. Suba o RabbitMQ localmente</h3>
<pre><code>
sudo docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 \
-e RABBITMQ_DEFAULT_USER=app -e RABBITMQ_DEFAULT_PASS=app123 -e RABBITMQ_DEFAULT_VHOST=app_vhost \
rabbitmq:3-management
</code></pre>

<h3>5. Execute a API</h3>
<pre><code>
uvicorn app.main:app --reload
</code></pre>
<p>A API estará disponível em: <a href="http://localhost:8000">http://localhost:8000</a></p>

<h3>6. Execute o Worker</h3>
<pre><code>
export AMQP_URL="amqp://app:app123@localhost:5672/app_vhost"
export QUEUE="tarefas.servimed"
python -m app.worker
</code></pre>

<hr>

<h2>🔐 Autenticação (Callback)</h2>

<p>O robô envia os dados extraídos para um endpoint de callback com <strong>token de autenticação</strong> via header <code>Authorization</code>.</p>

<h4>Exemplo de Header:</h4>
<pre><code>
Authorization: Bearer &lt;seu_token_aqui&gt;
</code></pre>

<hr>

<h2>📥 Exemplo de Requisição à API</h2>

<h3>POST <code>/task</code></h3>
<pre><code>
{
  "url": "https://example.com",
  "callback_url": "https://webhook.site/abc123",
  "auth_token": "seu_token_secreto"
}
</code></pre>

<hr>

<h2>✅ Status</h2>

<table>
  <thead>
    <tr><th>Etapa</th><th>Status</th></tr>
  </thead>
  <tbody>
    <tr><td>API com FastAPI</td><td>✅ Concluído</td></tr>
    <tr><td>RabbitMQ para enfileiramento</td><td>✅ Concluído</td></tr>
    <tr><td>Worker com Playwright</td><td>✅ Concluído</td></tr>
    <tr><td>Callback autenticado</td><td>✅ Concluído</td></tr>
    <tr><td>Deploy (Docker/Futuro)</td><td>✅ Concluído</td></tr>
  </tbody>
</table>

<hr>

<h2>✍️ Autor</h2>

<p>Desenvolvido por <strong>Arthur Inácio</strong><br>
<a href="https://github.com/arth-inacio">GitHub</a> |
<a href="https://www.linkedin.com/in/arth-inacio/">LinkedIn</a>
</p>
