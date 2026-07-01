# ==========================================================
#  recherche_ebay.py  -  Recherche d'annonces sur eBay
# ==========================================================
#  Rôle : interroger eBay pour trouver les annonces de
#  cartes Pokémon des séries surveillées, puis renvoyer
#  une liste d'annonces sous forme simple (titre, prix, lien).
#
#  Note : on lit les pages de résultats publiques d'eBay.
#  C'est simple pour démarrer ; on pourra passer à l'API
#  officielle eBay plus tard si besoin.
# ==========================================================

import requests
from bs4 import BeautifulSoup
import config


def construire_url(mot_cle):
    """
    Construit l'URL de recherche eBay pour un mot-clé donné.
    On trie par annonces les plus récentes.
    """
    mot_cle_url = mot_cle.replace(" ", "+")
    return (
        f"https://www.ebay.fr/sch/i.html"
        f"?_nkw={mot_cle_url}"
        f"&_sop=10"  # tri : plus récentes d'abord
    )


def nettoyer_prix(texte_prix):
    """
    Transforme un texte de prix eBay ('12,50 EUR') en nombre (12.50).
    Renvoie None si on n'arrive pas à lire le prix.
    """
    if not texte_prix:
        return None
    # On garde chiffres, virgules et points
    texte = texte_prix.replace("EUR", "").replace("€", "").strip()
    texte = texte.split("à")[0].split("to")[0].strip()  # ignore les fourchettes
    texte = texte.replace(",", ".")
    caracteres_ok = "0123456789."
    texte_filtre = "".join(c for c in texte if c in caracteres_ok)
    try:
        return round(float(texte_filtre), 2)
    except ValueError:
        return None


def chercher(mot_cle):
    """
    Cherche les annonces eBay pour un mot-clé.
    Renvoie une liste de dictionnaires :
    { 'titre', 'prix', 'lien', 'source' }
    """
    url = construire_url(mot_cle)
    entetes = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    annonces = []
    try:
        reponse = requests.get(url, headers=entetes, timeout=20)
        reponse.raise_for_status()
    except requests.RequestException as e:
        print(f"⚠️ Erreur de connexion à eBay : {e}")
        return annonces

    soup = BeautifulSoup(reponse.text, "html.parser")
    resultats = soup.select("li.s-item")

    for item in resultats:
        balise_titre = item.select_one(".s-item__title")
        balise_prix = item.select_one(".s-item__price")
        balise_lien = item.select_one("a.s-item__link")

        if not (balise_titre and balise_prix and balise_lien):
            continue

        titre = balise_titre.get_text(strip=True)
        prix = nettoyer_prix(balise_prix.get_text(strip=True))
        lien = balise_lien.get("href", "")

        # On ignore les lignes vides ou le bandeau "Shop on eBay"
        if titre.lower() in ("shop on ebay", ""):
            continue

        annonces.append({
            "titre": titre,
            "prix": prix,
            "lien": lien,
            "source": "eBay"
        })

    return annonces


def chercher_toutes_series():
    """
    Lance une recherche pour chaque série surveillée
    et regroupe toutes les annonces trouvées.
    """
    toutes = []
    for serie in config.SERIES_SURVEILLEES:
        mot_cle = f"carte pokemon {serie}"
        print(f"🔍 Recherche eBay : {mot_cle}")
        toutes.extend(chercher(mot_cle))
    return toutes
