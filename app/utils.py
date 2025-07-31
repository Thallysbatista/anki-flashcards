# app/utils.py

import json
from datetime import datetime

def salvar_frases_json(frases: list, path: str = "frases.json") -> None:
    """
    Salva a lista de frases em um arquivo JSON.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(frases, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise IOError(f"Erro ao salvar o arquivo {path}: {e}")


def carregar_frases_json(path: str = "frases.json") -> list:
    """
    Carrega e retorna a lista de frases do arquivo JSON.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise IOError(f"Erro ao carregar o arquivo {path}: {e}")
