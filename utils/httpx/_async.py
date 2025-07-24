import asyncio
from httpx import AsyncClient, Cookies, Request, Response, AsyncHTTPTransport
from httpx import Proxy
from logger import logger
from fake_useragent import FakeUserAgent


class AsyncHttpx:
    """
    Instancia um client assíncrono já passando as configurações padrões.
    """
    session: AsyncClient

    def __init__(
        self,
        spider_name: str,
        delay: float = 0.2,
        retries: int = 3,
    ):
        self.spider_name = spider_name
        user_agent = ""
        try:
            user_agent = FakeUserAgent().random.strip()
        except Exception:
            logger.exception("Não foi possível alterar o user-agent!")

        # Determina o transport utilizado para as requisições
        transport = AsyncHTTPTransport(
            verify=False,
            http2=True,
            retries=retries,
        )

        self.session = AsyncClient(
            transport=transport,
            headers={
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "pt-BR,en-US;q=0.9,en;q=0.8",
                "Connection": "keep-alive",
                "User-Agent": user_agent,
            },
            follow_redirects=True,
            timeout=200,
            verify=False,
            http2=True,
        )

        self.session.cookies = Cookies()

        # Hooks relacionados às requisições enviadas
        self.session.event_hooks["request"].append(self.to_http2)
        self.session.event_hooks["request"].append(self.rotate_useragent)
        self.session.event_hooks["request"].append(
            lambda _: self.delay_request(delay)
        )

        # Hooks relacionados às respostas
        self.session.event_hooks["response"].append(self.check_response)
        self.session.event_hooks["response"].append(self.raise_error)

    def __del__(self) -> None:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.session.aclose())
            else:
                loop.run_until_complete(self.session.aclose())
        except RuntimeError:
            logger.exception("[HTTPX] Erro ao fechar sessão!")

        logger.debug(f"[HTTPX] Fechando sessão de '{self.spider_name}'!")

    async def to_http2(self, request: Request) -> None:
        """
        Verifica se o certificado da requisição é https.
        Se for seta o http2 com True
        """
        setattr(self.session, "http2", "https" == request.url.scheme)

    async def check_response(self, res: Response) -> None:
        """
        Verifica se a resposta da requisição foi bem sucedida.

        :param res: resultado da requisição executada.
        """
        if not res:
            return

        req_method = res.request.method
        status, url, http = res.status_code, res.url, res.http_version
        logger.debug(
            f"\033[1;92m{self.spider_name}\033[0m | \033[1;90m({req_method})\033[0m {url} [{status}] | {http}"
        )

    @staticmethod
    async def raise_error(res: Response) -> None:
        """
        Levanta uma Exception se a requisição não for bem sucedida.
        :param res: resultado da requisição executada.
        """

        status, url = res.status_code, res.url

        if status >= 400:
            logger.error(f"Falha na requisição: {url} [{status}]")

        if status in [429, 503, 500, 502]:
            logger.warning("Aguardando 2 segundos...")
            await asyncio.sleep(2)

    @staticmethod
    async def rotate_useragent(req: Request) -> None:
        """Troca o user-agent em cada requisição."""
        try:
            req.headers["User-Agent"] = FakeUserAgent().random.strip()
        except Exception:
            logger.exception("Não foi possível alterar o user-agent!")

    @staticmethod
    async def delay_request(delay: float = 0.2) -> None:
        """Adiciona um delay em todas as requisições para saúde dos portais."""
        await asyncio.sleep(delay)