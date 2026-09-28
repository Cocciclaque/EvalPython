def check(chemin: str):
    with open(chemin, "r", encoding="utf-8") as fichier:
        for numero, ligne in enumerate(fichier, start=1):
            print(f"{numero:>4} | {ligne.rstrip()}")