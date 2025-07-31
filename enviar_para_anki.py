import os
import json
import requests

# Configurações
BARALHO = "TTS Inglês"
MODELO = "Basic"
PASTA_AUDIO = "audios"
TAG = "tts"

# 1. Lê as frases
with open("frases.json", "r", encoding="utf-8") as f:
    frases = json.load(f)

# 2. Garante que o baralho existe
requests.post("http://localhost:8765", json={
    "action": "createDeck",
    "version": 6,
    "params": { "deck": BARALHO }
})

# 3. Para cada frase, cria um card com áudio
for idx, frase in enumerate(frases, start=1):
    audio_filename = f"audio_{idx:03}.mp3"
    audio_path = os.path.join(PASTA_AUDIO, audio_filename)

    if not os.path.exists(audio_path):
        print(f"⚠️ Áudio não encontrado: {audio_path}")
        continue

    # Conteúdo do card
    front = f"{frase['ingles']}"
    back = frase["portugues"]

    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": BARALHO,
                "modelName": MODELO,
                "fields": {
                    "Front": front,
                    "Back": back
                },
                "options": {
                    "allowDuplicate": False
                },
                "tags": [TAG],
                "audio": [{
                    "path": os.path.abspath(audio_path),
                    "filename": audio_filename,
                    "fields": ["Front"]
                }]
            }
        }
    }

    response = requests.post("http://localhost:8765", json=payload)
    data = response.json()

    if data.get("error") == "cannot create note because it is a duplicate":
        print(f"🔁 Card {idx} ignorado (já existe no Anki).")
    elif data.get("error"):
        print(f"❌ Erro ao adicionar card {idx}: {data['error']}")
    else:
        print(f"✅ Card {idx} adicionado ao baralho '{BARALHO}'")

