# ==========================================================
#  recherche_vinted.py  -  Recherche d'annonces sur Vinted
# ==========================================================
#  Rôle : interroger Vinted pour trouver les annonces de
#  cartes Pokémon des séries surveillées, puis renvoyer
#  une liste d'annonces simples (titre, prix, lien).
#
#  Note : Vinted utilise une API interne au format JSON.
#  Il faut d'abord obtenir un "cookie de session" en
#  visitant le site, puis on interroge cette API.
# ==========================================================

import requests
import config


def obtenir_session():
    """
    Crée une session et récupère les cookies Vinted
    nécessaires pour interroger l'API interne.
    Renvoie l'objet session (ou None en cas d'échec).
    """
    session = requests.Session()
    entetes = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }
    session.headers.update(entetes)

    try:
        # Visiter la page d'accueil pour obtenir les cookies
        session.get("https://www.vinted.fr", timeout=20)
        return session
    except requests.RequestException as e:
        print(f"⚠️ Impossible d'ouvrir une session Vinted : {e}")
        return None


def nettoyer_prix(valeur):
    """
    Transforme un prix Vinted en nombre (float).
    Renvoie None si illisible.
    """
    if valeur is None:
        return None
    try:
        return round(float(valeur), 2)
    except (ValueError, TypeError):
        return None


def chercher(mot_cle, session=None):
    """
    Cherche les annonces Vinted pour un mot-clé.
    Renvoie une liste de dictionnaires :
    { 'titre', 'prix', 'lien', 'source' }
    """
    if session is None:
        session = obtenir_session()
    if session is None:
        return []

    annonces = []
    url_api = "https://www.vinted.fr/api/v2/catalog/items"
    params = {
        "search_text": mot_cle,
        "order": "newest_first",
        "per_page": 20
    }

    try:
        reponse = session.get(url_api, params=params, timeout=20)
        reponse.raise_for_status()
        donnees = reponse.json()
    except requests.RequestException as e:
        print(f"⚠️ Erreur de connexion à Vinted : {e}")
        return annonces
    except ValueError:
        print("⚠️ Réponse Vinted illisible (pas du JSON).")
        return annonces

    articles = donnees.get("items", [])
    for article in articles:
        titre = article.get("title", "")

        # Le prix peut être un objet {'amount': '12.5'} ou un nombre
        prix_brut = article.get("price")
        if isinstance(prix_brut, dict):
            prix = nettoyer_prix(prix_brut.get("amount"))
        else:
            prix = nettoyer_prix(prix_brut)

        lien = article.get("url", "")

        annonces.append({
            "titre": titre,
            "prix": prix,
            "lien": lien,
            "source": "Vinted"
        })

    return annonces


def chercher_toutes_series():
    """
    Lance une recherche pour chaque série surveillée
    et regroupe toutes les annonces trouvées.
    """
    session = obtenir_session()
    toutes = []
    for serie in config.SERIES_SURVEILLEES:
        mot_cle = f"carte pokemon {serie}"
        print(f"🔍 Recherche Vinted : {mot_cle}")
        toutes.extend(chercher(mot_cle, session))
    return toutes
