import asyncio
from servimed_scraper import ServimedScraper

async def main():
    coletor = ServimedScraper("juliano@farmaprevonline.com.br", "a007299A")
    await coletor.playwright_start()
    await coletor._coletor_cadastros()
    await coletor.playwright_finish()
if __name__ == "__main__":
    asyncio.run(main())
