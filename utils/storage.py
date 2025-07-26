import json
from datetime import datetime
from pathlib import Path

def salvar_json_local(data: list[dict], nome_base: str) -> str:
    # Cria pasta data se não existir
    Path("data").mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    caminho = Path("data") / f"{nome_base}_{timestamp}.json"

    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[storage] arquivo salvo em: {caminho}")
    return str(caminho)