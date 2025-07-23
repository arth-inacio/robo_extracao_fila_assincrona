import asyncio
from coletor import Coletor

async def main():
    coletor = Coletor("usuario", "senha")
    await coletor._coletor_cadastros()

if __name__ == "__main__":
    asyncio.run(main())
