# app/generator.py

import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from app.utils import salvar_frases_json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gerar_frases(n=5, verbo="get", model="gpt-3.5-turbo", salvar=False):
    prompt = f"""
Gere {n} frases em inglês sobre situações cotidianas de trabalho utilizando o verbo "{verbo}". 
Para cada frase, inclua a tradução em português. 
Responda exatamente no formato JSON abaixo, sem comentários ou texto extra, e sem vírgulas sobrando:

[
  {{"ingles": "Texto da frase em inglês", "portugues": "Tradução em português"}},
  ...
]
"""

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    content = response.choices[0].message.content

    try:
        raw = json.loads(content)
        frases = [{"en": item["ingles"], "pt": item["portugues"]} for item in raw]
    except Exception as e:
        raise ValueError(f"Erro ao processar JSON da resposta: {e}")

    if salvar:
        salvar_frases_json(frases)

    return frases
