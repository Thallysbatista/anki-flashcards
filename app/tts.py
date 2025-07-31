# Ler a lista de frases (en)
# Gerar um .mp3 para cada uma com voz neural
# Salvar em audios/
# Nomear os arquivos de forma única (pode ser com hash ou número sequencial)

# app/tts.py

import os
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # ID padrão (Rachel), pode ser parametrizado depois
OUTPUT_DIR = "audios"

headers = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json",
    "Accept": "audio/mpeg"
}


def gerar_nome_arquivo(texto: str) -> str:
    """
    Gera um nome de arquivo único com base no texto da frase.
    """
    hash_id = hashlib.md5(texto.encode("utf-8")).hexdigest()
    return f"{hash_id}.mp3"


def gerar_audios(frases: list) -> list:
    """
    Recebe uma lista de frases (com chave 'en') e gera arquivos de áudio usando ElevenLabs.
    Retorna a lista de caminhos gerados.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    paths = []

    for frase in frases:
        texto = frase["en"]
        nome_arquivo = gerar_nome_arquivo(texto)
        caminho = os.path.join(OUTPUT_DIR, nome_arquivo)

        # Pula se já existe
        if os.path.exists(caminho):
            paths.append(caminho)
            continue

        body = {
            "text": texto,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        response = requests.post(
            f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
            headers=headers,
            json=body
        )

        if response.status_code == 200:
            with open(caminho, "wb") as f:
                f.write(response.content)
            paths.append(caminho)
        else:
            print(f"Erro ao gerar áudio para: {texto} → {response.status_code}")
            print(response.text)

    return paths
