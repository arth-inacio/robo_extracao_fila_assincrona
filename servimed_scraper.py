import re
import json
from utils.storage import salvar_json_local
from playwright.async_api import async_playwright, TimeoutError

class ServimedScraper:
    usuario: str
    senha: str
    url = "https://pedidoeletronico.servimed.com.br/"

    def __init__(self, usuario: str, senha: str) -> None:
        self.usuario = usuario
        self.senha = senha
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def playwright_start(self) -> None:
        # Método que Inicializa o playwright
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        self.page.set_default_timeout(40000)

    async def playwright_finish(self) -> None:
        # Finaliza a sessão do playwright
        await self.context.close()
        await self.playwright.stop()
        await self.browser.close()

    async def _coletor_cadastros(self) -> list[dict]:
        itens = []
        await self.page.goto(f"{self.url}login")
        await self.page.wait_for_load_state("networkidle")

        await self.page.type("input[name=\"username\"]", self.usuario)
        await self.page.type("input[name=\"password\"]", self.senha)

        # Clica no botao de login
        await self.page.locator("button[class=\"btn btn-block btn-success\"]").click()
        await self.page.wait_for_selector("button[class=\"swal2-cancel swal2-styled\"]")

        # Cancela o alerta de atualização dos dados
        await self.page.locator("button[class=\"swal2-cancel swal2-styled\"]").click()
        await self.page.wait_for_load_state("networkidle")

        # Clica em pedidos -> novo pedido
        await self.page.locator("a").filter(has_text="Pedidos").click()
        await self.page.wait_for_load_state("networkidle")
        await self.page.get_by_role("link", name="Novo pedido").click()

        await self.page.get_by_role("link", name="refresh Alterar").click()
        await self.page.wait_for_load_state("networkidle")

        # Seleciona cliente com lista de produtos
        await self.page.get_by_text("267511").click()
        await self.page.wait_for_load_state("networkidle")

        # Preenche o campo de pesquisa de produtos
        await self.page.locator("input[role=\"combobox\"]").fill("PARACETAMOL")

        # Clica no botao pesquisar e procura a requisição com os produtos
        async with self.page.expect_response(re.compile(r"carrinho/oculto")) as response_info:
            await self.page.click("//html/body/app-root/pedido/div[4]/div/div[1]/div/div/div[3]/button/i")
        response = await response_info.value
        body = await response.body()

        registros_dict  = json.loads(body)
        produtos = registros_dict.get("lista", [])

        for produto in produtos:
            informacoes = {
                "ean": produto["codigoBarras"],
                "codigo": produto["id"],
                "descricao": produto["descricao"],
                "preco_fabrica": produto["valorBase"],
                "estoque": produto["quantidadeEstoque"],
            }
            itens.append(informacoes)

        salvar_json_local(itens, "produtos")
        return itens