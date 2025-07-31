import logging
import re
import json
from utils.storage import salvar_json_local
from playwright.async_api import async_playwright, TimeoutError
from typing import Any, Dict, List

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

    async def _coletor_cadastros(self, termo_busca: str, cliente: str) -> list[dict]:
        itens = []
        for _ in range(3):
            await self.page.goto(f"{self.url}login")
            await self.page.wait_for_load_state("networkidle")

            await self.page.type("input[name=\"username\"]", self.usuario)
            await self.page.type("input[name=\"password\"]", self.senha)

            try:
                # Clica no botao de login
                await self.page.locator("button[class=\"btn btn-block btn-success\"]").click()
                await self.page.wait_for_selector("button[class=\"swal2-cancel swal2-styled\"]")
                await self.page.wait_for_load_state("networkidle")

                # Cancela o alerta de atualização dos dados
                await self.page.locator("button[class=\"swal2-cancel swal2-styled\"]").click()
                await self.page.wait_for_load_state("networkidle")
            except TimeoutError:
                continue
            break

        # Clica em pedidos -> novo pedido
        await self.page.locator("a").filter(has_text="Pedidos").click()
        await self.page.wait_for_load_state("networkidle")
        await self.page.get_by_role("link", name="Novo pedido").click()

        await self.page.get_by_role("link", name="refresh Alterar").click()
        await self.page.wait_for_load_state("networkidle")

        # Seleciona cliente com lista de produtos
        await self.page.get_by_text(cliente).click()
        await self.page.wait_for_load_state("networkidle")

        # Preenche o campo de pesquisa de produtos
        await self.page.locator("input[role=\"combobox\"]").fill(termo_busca)

        # Clica no botao pesquisar e procura a requisição com os produtos
        async with self.page.expect_response(re.compile(r"carrinho/oculto")) as response_info:
            await self.page.click("//html/body/app-root/pedido/div[4]/div/div[1]/div/div/div[3]/button/i")
        response = await response_info.value
        body = await response.body()

        registros_dict  = json.loads(body)
        produtos = registros_dict.get("lista", [])

        for produto in produtos:
            informacoes = {
                "gtin": produto["codigoBarras"],
                "codigo": produto["id"],
                "descricao": produto["descricao"],
                "preco_fabrica": produto["valorBase"],
                "estoque": produto["quantidadeEstoque"],
            }
            itens.append(informacoes)

        salvar_json_local(itens, "produtos")
        return itens
    
    async def collect_products(self, termo_busca: str = "PARACETAMOL", cliente: str = "267511") -> List[Dict[str, Any]]:
        await self.playwright_start()
        try:
            print(f"[SCRAPER] Iniciando busca: termo_busca={termo_busca}, cliente={cliente}")
            produtos = await self._coletor_cadastros(termo_busca=termo_busca, cliente=cliente)
            logging.info("[SCRAPER] Produtos encontrados: %s", produtos)
            return produtos
        finally:
            await self.playwright_finish()