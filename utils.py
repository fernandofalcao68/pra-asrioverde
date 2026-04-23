import json
import os

ARQ_DADOS = "dados.json"
ARQ_USUARIOS = "usuarios.json"

BG = "#121212"
CARD = "#1f1f1f"
TXT = "white"


def carregar_json(arq):
    if not os.path.exists(arq):
        return []
    with open(arq, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_json(arq, dados):
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)