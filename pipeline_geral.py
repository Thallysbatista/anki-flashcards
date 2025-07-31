import subprocess
import sys

# Garante que todos os subprocessos usem o Python da venv atual
PYTHON = sys.executable

print("📌 Iniciando pipeline completo...\n")

# Etapa 1 – Gerar frases com LLM
print("🧠 Gerando frases com LLM...")
subprocess.run([PYTHON, "gerar_frases.py"])

# Etapa 2 – Gerar áudios
print("\n🔊 Gerando áudios com ElevenLabs...")
subprocess.run([PYTHON, "gerar_audios_para_frases.py"])

# Etapa 3 – Enviar para o Anki
print("\n🧠 Criando flashcards no Anki...")
subprocess.run([PYTHON, "enviar_para_anki.py"])

print("\n✅ Pipeline finalizado com sucesso!")
