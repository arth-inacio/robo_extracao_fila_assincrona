from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.coletor.servimed_scraper import ServimedScraper

app = FastAPI()

class ScrapRequest(BaseModel):
    usuario: str
    senha: str

@app.post("/scrap")
async def scrap(request: ScrapRequest):
    try:
        scraper = ServimedScraper(request.usuario, request.senha)
        await scraper.playwright_start()
        try:
            produtos = await scraper._coletor_cadastros("PARACETAMOL", "267511")
        except Exception as e:
            produtos = []
        await scraper.playwright_finish()
        return {"produtos": produtos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))