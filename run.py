import asyncio
from servimed_scraper import ServimedScraper

async def main():
    coletor = ServimedScraper("usuario", "senha")
    await coletor._coletor_cadastros()

if __name__ == "__main__":
    asyncio.run(main())
