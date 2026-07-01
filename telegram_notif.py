# ==========================================================
#  telegram_notif.py  -  Envoi des alertes sur Telegram
# ==========================================================
#  Rôle : envoyer un message Telegram quand une bonne
#  affaire est trouvée. Utilise l'API des bots Telegram.
# ==========================================================

import requests
import config


def envoyer_message(texte):
    """
    Envoie un message texte sur votre chat Telegram.
    Renvoie True si l'envoi a réussi, False sinon.
    """
    # On vérifie que la config est bien remplie
    if not config.TELEGRAM_TOKEN or not config.TELEGRAM_CHAT_ID:
        print("⚠️ Token ou Chat ID Telegram manquant dans config.py")
        return False

    url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
    donnees = {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": texte,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    try:
        reponse = requests.post(url, data=donnees, timeout=15)
        if reponse.status_code == 200:
            return True
        else:
            print(f"⚠️ Telegram a répondu avec le code {reponse.status_code}")
            print(reponse.text)
            return False
    except requests.RequestException as e:
        print(f"⚠️ Erreur d'envoi Telegram : {e}")
        return False


def alerte_bonne_affaire(titre, prix, cote, prix_revente, lien, source):
    """
    Met en forme puis envoie une alerte 'bonne affaire'.
    - titre        : nom de la carte / de l'annonce
    - prix         : prix de l'annonce
    - cote         : cote médiane calculée
    - prix_revente : prix de revente visé
    - lien         : URL de l'annonce
    - source       : 'eBay', 'Vinted'...
    """
    # Calcul du gain potentiel
    if cote and prix:
        marge = round(prix_revente - prix, 2)
    else:
        marge = "?"

    texte = (
        f"🎴 <b>BONNE AFFAIRE REPÉRÉE !</b>\n\n"
        f"📌 <b>{titre}</b>\n"
        f"🏷️ Source : {source}\n\n"
        f"💰 Prix annonce : <b>{prix} €</b>\n"
        f"📊 Cote médiane : {cote} €\n"
        f"📈 Revente visée : {prix_revente} €\n"
        f"✨ Marge estimée : <b>{marge} €</b>\n\n"
        f"🔗 <a href=\"{lien}\">Voir l'annonce</a>"
    )

    return envoyer_message(texte)


def message_demarrage():
    """Petit message pour confirmer que le bot est bien lancé."""
    return envoyer_message("✅ Le bot Pokémon est démarré et surveille les annonces !")
