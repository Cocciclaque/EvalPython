from typing import Literal
import json

from ollama import ResponseError, chat
from pydantic import BaseModel, Field, ValidationError

MODELE = "llama3.2:3b"

CONSIGNE = (
    "Tu es un assistant de support client pour un jeu vidéo. "
    "Analyse le ticket du joueur et réponds uniquement en JSON avec : "
    "category (bug, payment, account, suggestion, toxicity, autre), "
    "severity (entier de 1 à 5, 5 étant le plus urgent), "
    "sentiment (positive, neutral, negative), "
    "summary (une phrase courte résumant le ticket)."
)


class TriageError(Exception):
    """Erreur bloquante, avec un message lisible par l'utilisateur."""


class Analyse(BaseModel):
    category: Literal["bug", "payment", "account", "suggestion", "toxicity", "autre"]
    severity: int = Field(ge=1, le=5)
    sentiment: Literal["positive", "neutral", "negative"]
    summary: str


def charger_tickets(chemin:str):
    try:
        with open(chemin, "r", encoding="utf-8") as fichier:
            tickets = json.load(fichier)
    except FileNotFoundError:
        raise TriageError(f"Fichier de tickets introuvable : {chemin}") from None
    except json.JSONDecodeError as erreur:
        raise TriageError(
            f"JSON mal formé dans {chemin} (ligne {erreur.lineno}, colonne {erreur.colno})."
        ) from None
    if not isinstance(tickets, list):
        raise TriageError(f"{chemin} doit contenir une liste de tickets.")
    return tickets


def message_utilisable(ticket:object):
    if not isinstance(ticket, dict):
        return False
    message = ticket.get("message")
    return isinstance(message, str) and message.strip() != ""


def interroger_llm(message:str):
    try:
        reponse = chat(
            model=MODELE,
            messages=[
                {"role": "system", "content": CONSIGNE},
                {"role": "user", "content": message},
            ],
            format=Analyse.model_json_schema(),
        )
    except ConnectionError:
        raise TriageError("Impossible de joindre Ollama : lance l'application Ollama puis réessaie.") from None
    except ResponseError as erreur:
        raise TriageError(f"Ollama a renvoyé une erreur : {erreur.error}") from None
    return reponse.message.content


def valider(contenu:str):
    try:
        return Analyse.model_validate_json(contenu).model_dump()
    except ValidationError:
        return None


def sauvegarder(resultats:list[dict], chemin:str):
    try:
        with open(chemin, "w", encoding="utf-8") as fichier:
            json.dump(resultats, fichier, ensure_ascii=False, indent=2)
    except OSError as erreur:
        raise TriageError(f"Impossible d'écrire {chemin} : {erreur.strerror}") from None


def trier(chemin_entree: str, chemin_sortie: str):
    resultats = []
    for ticket in charger_tickets(chemin_entree):
        if not message_utilisable(ticket):
            print(f"Ticket ignoré (message absent ou vide) : {ticket}")
            pass
        analyse = valider(interroger_llm(ticket["message"]))
        statut = "ok" if analyse else "to_check"
        resultats.append({"ticket": ticket, "analyse": analyse, "statut": statut})
    sauvegarder(resultats, chemin_sortie)