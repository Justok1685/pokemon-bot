# ==========================================================
#  main.py  -  Chef d'orchestre du bot Pokémon
# ==========================================================
#  Rôle : faire tourner le bot en boucle.
#  À chaque cycle :
#    1. Chercher les annonces (eBay + Vinted)
#    2. Filtrer les annonces déjà vues (doublons)
#    3. Calculer la cote médiane de chaque carte
#    4. Garder les bonnes affaires (marge suffisante)
#    5. Envoyer une alerte Telegram
#    6. Mémoriser les annonces traitées
# ==========================================================

import time

import config
import etat
import cotes
import filtres
import telegram_notif
import recherche_ebay
import recherche_vinted


def traiter_annonce(annonce):
    """
    Traite une seule annonce :
    - vérifie les filtres
    - calcule la cote
    - décide si c'est une bonne affaire
    - envoie l'alerte Telegram si oui
    """
    titre = annonce.get("titre", "")
    prix = annonce.get("prix")
    lien = annonce.get("lien", "")
    source = annonce.get("source", "?")

    # 1) On ignore les annonces déjà vues
    if etat.deja_vue(lien):
        return

    # 2) Filtres de base (prix présent, mots-clés, etc.)
    if not filtres.annonce_valide(annonce):
        etat.marquer_vue(lien)  # on la mémorise pour ne pas la re-tester
        return

    # 3) Calcul de la cote médiane
    cote = cotes.cote_mediane(titre)
    if not cote:
        etat.marquer_vue(lien)
        return

    # 4) Décision : bonne affaire ?
    prix_revente = round(cote * config.COEFF_REVENTE, 2)
    if filtres.est_bonne_affaire(prix, cote):
        telegram_notif.alerte_bonne_affaire(
            titre=titre,
            prix=prix,
            cote=cote,
            prix_revente=prix_revente,
            lien=lien,
            source=source
        )
        print(f"✅ BONNE AFFAIRE : {titre} ({prix} € / cote {cote} €)")

    # 5) Dans tous les cas, on mémorise l'annonce
    etat.marquer_vue(lien)


def un_cycle():
    """Effectue un cycle complet de recherche et de traitement."""
    print("\n===== NOUVEAU CYCLE =====")

    annonces = []
    annonces.extend(recherche_ebay.chercher_toutes_series())
    annonces.extend(recherche_vinted.chercher_toutes_series())

    print(f"📦 {len(annonces)} annonces récupérées au total.")

    for annonce in annonces:
        traiter_annonce(annonce)

    # On sauvegarde l'état (annonces vues) sur le disque
    etat.sauvegarder()
    print("💾 État sauvegardé.")


def demarrer():
    """Lance le bot en boucle infinie."""
    print("🤖 Démarrage du bot Pokémon...")
    etat.charger()  # on récupère les annonces déjà vues
    telegram_notif.message_demarrage()

    while True:
        try:
            un_cycle()
        except Exception as e:
            print(f"⚠️ Erreur pendant le cycle : {e}")

        print(f"⏳ Pause de {config.INTERVALLE_MINUTES} minutes...\n")
        time.sleep(config.INTERVALLE_MINUTES * 60)


if __name__ == "__main__":
    demarrer()
