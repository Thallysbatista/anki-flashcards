import os
import requests
import json
from dotenv import load_dotenv

# Carrega a chave da ElevenLabs do .env
load_dotenv()
API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel

# Carrega o arquivo com as frases geradas pelo LLM
with open("frases.json", "r", encoding="utf-8") as f:
    frases = json.load(f)

# Gera um áudio para cada frase
for idx, frase in enumerate(frases, start=1):
    texto = frase["ingles"]
    filename = os.path.join("audios", f"audio_{idx:03}.mp3")

    body = {
        "text": texto,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.8
        }
    }

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    response = requests.post(url, headers=headers, json=body)

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Áudio gerado: {filename}")
    else:
        print(f"❌ Erro ao gerar áudio para: {texto}")
        print(f"Código {response.status_code} - {response.text}")
