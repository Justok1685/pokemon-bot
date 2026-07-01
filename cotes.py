# ==========================================================
#  cotes.py  -  Calcul de la cote médiane d'une carte
# ==========================================================
#  La "cote" = prix de référence d'une carte.
#  On la calcule comme la MÉDIANE des prix récents observés
#  sur eBay et Cardmarket. La médiane est plus robuste que
#  la moyenne : un prix aberrant ne la fausse pas.
# ==========================================================

import statistics


def calculer_mediane(liste_prix):
    """Renvoie la médiane d'une liste de prix (nombres).
    Renvoie None si la liste est vide."""
    prix_valides = [p for p in liste_prix if p is not None and p > 0]
    if not prix_valides:
        return None
    return round(statistics.median(prix_valides), 2)


def calculer_cote(prix_ebay, prix_cardmarket):
    """
    Calcule la cote médiane d'une carte.
    - prix_ebay        : liste de prix récents constatés sur eBay
    - prix_cardmarket  : liste de prix récents constatés sur Cardmarket
    On réunit les deux sources puis on prend la médiane globale.
    Renvoie None si on n'a aucune donnée.
    """
    tous_les_prix = []
    if prix_ebay:
        tous_les_prix.extend(prix_ebay)
    if prix_cardmarket:
        tous_les_prix.extend(prix_cardmarket)

    return calculer_mediane(tous_les_prix)


def prix_achat_max(cote, seuil_achat):
    """
    Prix maximum auquel on accepte d'ACHETER.
    Ex : cote 20€, seuil 0.10 -> on achète si <= 18€.
    """
    if cote is None:
        return None
    return round(cote * (1 - seuil_achat), 2)


def prix_revente_min(cote, seuil_revente):
    """
    Prix minimum auquel on vise la REVENTE.
    Ex : cote 20€, seuil 0.10 -> on revend à >= 22€.
    """
    if cote is None:
        return None
    return round(cote * (1 + seuil_revente), 2)


def est_bonne_affaire(prix_annonce, cote, seuil_achat):
    """
    Renvoie True si le prix de l'annonce est une bonne affaire,
    c'est-à-dire au moins 'seuil_achat' SOUS la cote.
    """
    if cote is None or prix_annonce is None:
        return False
    seuil = prix_achat_max(cote, seuil_achat)
    return prix_annonce <= seuil
