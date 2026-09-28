from ollama import ResponseError, chat
from pydantic import BaseModel, Field, ValidationError
import json

MODELE = "llama3.2:3b"

CONSIGNE = (
    "Tu es un assistant de support client pour un jeu vidéo. "
    "Analyse le ticket du joueur et génère un brouillon de réponse. "
    "La réponse doit être polie, adaptée et rédigée dans la langue du joueur"
)

def interroger_llm_text(message:str):
    reponse = chat(
        model=MODELE,
        messages=[
            {"role": "system", "content": CONSIGNE},
            {"role": "user", "content": message},
        ]
    )
    return reponse.message.content

def make_draft(filepath:str):
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
        for line in data:
            with open("draft_" +line["ticket"]["id"], "w", encoding="utf-8") as draft:
                draft.write(interroger_llm_text(line["ticket"]["message"]))
                draft.close()