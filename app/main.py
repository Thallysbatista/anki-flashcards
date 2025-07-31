# app/main.py

import os
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse
from app.generator import gerar_frases
from app.tts import gerar_audios
from app.utils import carregar_frases_json
from app.anki_builder import gerar_deck
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request  

# Garante que a pasta decks exista ANTES de montar os arquivos estáticos
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
async def generate_audios():
    try:
        frases = carregar_frases_json()
        caminhos = gerar_audios(frases)
        nomes_arquivos = [os.path.basename(c) for c in caminhos]

        return {
            "quantidade": len(nomes_arquivos),
            "arquivos": nomes_arquivos
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/generate-deck")
async def generate_deck():
    try:
        caminho = gerar_deck()
        nome_arquivo = os.path.basename(caminho)
        return {
            "deck": nome_arquivo,
            "caminho": caminho
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# --------------------------------------------
# 📌 PIPELINE COMPLETA - GERAR DECK AUTOMATICAMENTE
# Este endpoint executa todas as etapas:
# 1. Gera frases com LLM (OpenAI)
# 2. Gera áudios com ElevenLabs
# 3. Cria um deck .apkg com frases + áudio
# Retorna o nome e caminho do deck gerado.
# --------------------------------------------

@app.get("/pipeline")
async def pipeline(
    request: Request,
    n: int = Query(5, ge=1, le=50),
    verbo: str = Query("get"),
    model: str = Query("gpt-3.5-turbo")
):
    try:
        frases = gerar_frases(n=n, verbo=verbo, model=model, salvar=True)
        caminhos_audios = gerar_audios(frases)

        if len(caminhos_audios) < len(frases):
            return JSONResponse(status_code=500, content={
                "error": "Nem todos os áudios foram gerados.",
                "frases": len(frases),
                "audios_gerados": len(caminhos_audios)
            })

        caminho_deck = gerar_deck()
        nome_deck = os.path.basename(caminho_deck)

        # Cria URL absoluta de download
        host_url = request.base_url._url.rstrip("/")
        deck_url = f"{host_url}/decks/{nome_deck}"

        return {
            "mensagem": "Pipeline executada com sucesso!",
            "modelo": model,
            "verbo": verbo,
            "quantidade_frases": n,
            "deck": nome_deck,
            "url_download": deck_url
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
    

# Servir arquivos estáticos: HTML + decks
# Servir os decks primeiro
app.mount("/decks", StaticFiles(directory="decks"), name="decks")
# Depois o HTML
app.mount("/", StaticFiles(directory="static", html=True), name="static")

