# ==========================================================
#  config.py  -  Réglages généraux du bot Pokémon
# ==========================================================
#  Ce fichier NE contient AUCUN mot de passe ni clé secrète.
#  Les clés sont lues depuis les "Secrets" GitHub (voir plus tard).
# ==========================================================

import os

# ----- CLÉS SECRÈTES (lues depuis les Secrets GitHub) -----
# Ne rien écrire ici ! Ces valeurs viennent des Secrets.
TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")
EBAY_APP_ID      = os.environ.get("EBAY_APP_ID", "")
EBAY_CERT_ID     = os.environ.get("EBAY_CERT_ID", "")

# ----- STRATÉGIE D'ACHAT / REVENTE -----
# On achète si le prix est au moins 10% SOUS la cote.
SEUIL_ACHAT = 0.10        # 10 %
# On vise une revente à au moins 10% AU-DESSUS de la cote.
SEUIL_REVENTE = 0.10      # 10 %

# ----- ÉTAT DES CARTES ACCEPTÉES -----
# On ne veut que du neuf ou "near mint".
ETATS_ACCEPTES = ["neuf", "near mint", "nm", "mint"]

# ----- SÉRIES SURVEILLÉES -----
SERIES_SURVEILLEES = ["151", "Méga Évolution"]

# ----- MOTS INTERDITS (pour exclure lots, coffrets, displays...) -----
# Si un de ces mots apparaît dans l'annonce, on l'IGNORE.
MOTS_INTERDITS = [
    "lot", "lots", "coffret", "coffrets", "display", "displays",
    "booster box", "boite", "boîte", "bundle", "ensemble",
    "collection", "x10", "x36", "carton", "scellé", "scelle"
]

# ----- FRÉQUENCE (informatif : le vrai timing est dans bot.yml) -----
DESCRIPTION_FREQUENCE = "Vérification toutes les 30 minutes environ"

# ----- DEVISE -----
DEVISE = "EUR"
