import os
import requests
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()
API_KEY = os.getenv("ELEVEN_API_KEY")

# ID da voz padrão (Rachel é bem natural)
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel

# Texto que queremos transformar em áudio
texto = "I'm analyzing the data to identify trends."

# Define o nome do arquivo de saída
output_filename = os.path.join("audios", "audio_001.mp3")


# Faz a requisição para a ElevenLabs
url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

headers = {
    "xi-api-key": API_KEY,
    "Content-Type": "application/json"
}

body = {
    "text": texto,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.4,
        "similarity_boost": 0.8
    }
}

response = requests.post(url, headers=headers, json=body)

# Salva o arquivo se a resposta for válida
if response.status_code == 200:
    with open(output_filename, "wb") as f:
        f.write(response.content)
    print(f"✅ Áudio salvo como {output_filename}")
else:
    print(f"❌ Erro: {response.status_code}")
    print(response.text)
