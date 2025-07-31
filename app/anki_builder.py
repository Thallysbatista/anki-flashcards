# app/anki_builder.py
# - Lê o frases.json
# - Verifica se os áudios existem
# - Gera o deck .apkg com genanki
# - Retorna o nome do arquivo gerado

import os
import time
import genanki
from app.utils import carregar_frases_json
from app.tts import gerar_nome_arquivo

DECKS_DIR = "decks"
AUDIO_DIR = "audios"

def gerar_deck(nome_deck: str = "Frases Inglês") -> str:
    """
    Cria um baralho .apkg a partir do frases.json e retorna o caminho do arquivo gerado.
    """

    # Garantir que pastas existem
    os.makedirs(DECKS_DIR, exist_ok=True)

    # ID fixo e nome para o deck e modelo
    deck_id = int(time.time())  # usa timestamp como ID único
    model_id = deck_id + 1

    model = genanki.Model(
        model_id,
        'ModeloComAudio',
        fields=[
            {'name': 'Frase'},
            {'name': 'Audio'},
            {'name': 'Traducao'}
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Frase}}<br>{{Audio}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Traducao}}'
            }
        ]
    )

    deck = genanki.Deck(deck_id, nome_deck)
    media_files = []

    frases = carregar_frases_json()

    for frase in frases:
        texto_en = frase["en"]
        texto_pt = frase["pt"]
        nome_audio = gerar_nome_arquivo(texto_en)
        caminho_audio = os.path.join(AUDIO_DIR, nome_audio)

        if not os.path.exists(caminho_audio):
            print(f"Áudio não encontrado para: {texto_en}")
            continue

        media_files.append(caminho_audio)

        note = genanki.Note(
            model=model,
            fields=[texto_en, f"[sound:{nome_audio}]", texto_pt]
        )

        deck.add_note(note)

    # Nome do arquivo final
    nome_arquivo = f"deck_{deck_id}.apkg"
    caminho_final = os.path.join(DECKS_DIR, nome_arquivo)

    genanki.Package(deck, media_files).write_to_file(caminho_final)

    return caminho_final
