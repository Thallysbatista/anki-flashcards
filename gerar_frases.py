import openai
import json
import os
from dotenv import load_dotenv

# Carrega variáveis do arquivo .env
load_dotenv()

# Pega a chave da variável de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

# Prompt para o modelo
prompt_usuario = """
Gere 5 frases em inglês sobre situações cotidianas de trabalho utilizando o verbo "get". Para cada frase, inclua a tradução em português. Responda **exatamente** no formato JSON abaixo, sem comentários ou texto extra, e sem vírgulas sobrando:

[
  {"ingles": "Texto da frase em inglês", "portugues": "Tradução em português"},
  ...
]
"""


# Enviar a requisição para o modelo
response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Você é um gerador de frases para flashcards."},
        {"role": "user", "content": prompt_usuario}
    ],
    temperature=0.5
)

# Tenta interpretar a resposta como JSON
try:
    result_text = response.choices[0].message.content.strip()

    # Remove blocos de markdown se existirem
    if result_text.startswith("```json"):
        result_text = result_text.replace("```json", "").replace("```", "").strip()

    frases = json.loads(result_text)

    # Salva no arquivo frases.json
    with open("frases.json", "w", encoding="utf-8") as f:
        json.dump(frases, f, ensure_ascii=False, indent=2)

    # Exibe no terminal
    for f in frases:
        print(f"- 🇺🇸 {f['ingles']}\n  🇧🇷 {f['portugues']}\n")

except Exception as e:
    print("Erro ao interpretar resposta do modelo:")
    print(result_text)
    print(e)

