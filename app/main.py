# app/main.py

import os
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.generator import gerar_frases
from app.tts import gerar_audios
from app.utils import carregar_frases_json
from app.anki_builder import gerar_deck

# Garante que a pasta `decks/` exista antes de montar os estáticos
os.makedirs("decks", exist_ok=True)

app = FastAPI(
    title="Anki Flashcards API",
    description="API para geração de frases, áudios e criação de flashcards no Anki",
    version="1.0.0"
)

@app.get("/healthcheck")
async def healthcheck():
    return JSONResponse(content={"status": "ok"})


@app.get("/generate-frases")
async def generate_frases(
    n: int = Query(5, ge=1, le=50),
    verbo: str = Query("get"),
    model: str = Query("gpt-3.5-turbo"),
    salvar: bool = Query(False)
):
    try:
        frases = gerar_frases(n=n, verbo=verbo, model=model, salvar=salvar)
        return {
            "modelo": model,
            "quantidade": n,
            "verbo": verbo,
            "salvo": salvar,
            "frases": frases
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/generate-audios")
async def generate_audios_endpoint():
    try:
        frases = carregar_frases_json()
        caminhos = gerar_audios(frases)
        nomes = [os.path.basename(c) for c in caminhos]
        return {"quantidade": len(nomes), "arquivos": nomes}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/generate-deck")
async def generate_deck_endpoint():
    try:
        caminho = gerar_deck()
        nome = os.path.basename(caminho)
        return {"deck": nome, "caminho": caminho}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# --------------------------------------------
# 📌 PIPELINE COMPLETA - GERAR DECK AUTOMATICAMENTE
# Este endpoint executa todas as etapas:
# 1. Gera frases com LLM (OpenAI)
# 2. Gera áudios com ElevenLabs
# 3. Cria um deck .apkg com frases + áudio
# Retorna o nome do deck e URL para download.
# --------------------------------------------

@app.get("/pipeline")
async def pipeline(
    request: Request,
    n: int = Query(5, ge=1, le=50),
    verbo: str = Query("get"),
    model: str = Query("gpt-3.5-turbo")
):
    try:
        # 1) gera frases e salva em frases.json
        frases = gerar_frases(n=n, verbo=verbo, model=model, salvar=True)

        # 2) gera áudios para cada frase
        caminhos_audios = gerar_audios(frases)
        if len(caminhos_audios) < len(frases):
            return JSONResponse(status_code=500, content={
                "error": "Nem todos os áudios foram gerados.",
                "frases": len(frases),
                "audios_gerados": len(caminhos_audios)
            })

        # 3) gera o deck .apkg
        caminho_deck = gerar_deck()
        nome_deck = os.path.basename(caminho_deck)

        # monta a URL pública de download
        host_url = request.base_url._url.rstrip("/")
        url_download = f"{host_url}/decks/{nome_deck}"

        return {
            "mensagem": "Pipeline executada com sucesso!",
            "modelo": model,
            "verbo": verbo,
            "quantidade_frases": n,
            "deck": nome_deck,
            "url_download": url_download
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# Servir arquivos estáticos:
# 1) pasta de decks (deve existir em /app/decks)
app.mount("/decks", StaticFiles(directory="decks"), name="decks")
# 2) front-end estático (index.html em /app/static)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
