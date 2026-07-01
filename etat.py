# ==========================================================
#  etat.py  -  Mémoire du bot (annonces vues, pause, compteurs)
# ==========================================================
#  Ce fichier lit et écrit un petit fichier "memoire.json"
#  pour se souvenir des choses d'une exécution à l'autre.
# ==========================================================

import json
import os

# Nom du fichier qui stocke la mémoire
FICHIER_MEMOIRE = "memoire.json"

# Structure par défaut si le fichier n'existe pas encore
MEMOIRE_PAR_DEFAUT = {
    "annonces_vues": [],   # liste des identifiants d'annonces déjà signalées
    "en_pause": False,     # le bot est-il en pause ?
    "nb_alertes_envoyees": 0
}


def charger_memoire():
    """Lit la mémoire depuis le fichier. Crée un état par défaut si absent."""
    if not os.path.exists(FICHIER_MEMOIRE):
        return dict(MEMOIRE_PAR_DEFAUT)
    try:
        with open(FICHIER_MEMOIRE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # Fichier corrompu ou illisible : on repart propre
        return dict(MEMOIRE_PAR_DEFAUT)


def sauver_memoire(memoire):
    """Écrit la mémoire dans le fichier."""
    with open(FICHIER_MEMOIRE, "w", encoding="utf-8") as f:
        json.dump(memoire, f, ensure_ascii=False, indent=2)


def deja_vue(memoire, identifiant):
    """Renvoie True si l'annonce a déjà été signalée."""
    return identifiant in memoire.get("annonces_vues", [])


def marquer_vue(memoire, identifiant):
    """Ajoute une annonce à la liste des annonces déjà vues."""
    if "annonces_vues" not in memoire:
        memoire["annonces_vues"] = []
    if identifiant not in memoire["annonces_vues"]:
        memoire["annonces_vues"].append(identifiant)
        # On limite la taille pour éviter que le fichier grossisse sans fin
        if len(memoire["annonces_vues"]) > 5000:
            memoire["annonces_vues"] = memoire["annonces_vues"][-5000:]


def est_en_pause(memoire):
    """Renvoie True si le bot est en pause."""
    return memoire.get("en_pause", False)


def mettre_en_pause(memoire, valeur=True):
    """Active ou désactive la pause."""
    memoire["en_pause"] = valeur
