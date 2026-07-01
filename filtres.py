# ==========================================================
#  filtres.py  -  Le "videur" : trie les annonces
# ==========================================================
#  Rôle : décider si une annonce mérite qu'on s'y intéresse.
#  On écarte les lots/coffrets/displays, les mauvais états,
#  et on ne garde que les séries surveillées.
# ==========================================================

import config


def contient_mot_interdit(titre):
    """
    Renvoie True si le titre contient un mot interdit
    (lot, coffret, display, scellé, etc.).
    """
    titre_min = titre.lower()
    for mot in config.MOTS_INTERDITS:
        if mot.lower() in titre_min:
            return True
    return False


def etat_accepte(texte):
    """
    Renvoie True si l'état mentionné est acceptable
    (neuf, near mint, mint...). Si aucun état n'est
    mentionné, on reste prudent et on renvoie False.
    """
    if not texte:
        return False
    texte_min = texte.lower()
    for etat in config.ETATS_ACCEPTES:
        if etat.lower() in texte_min:
            return True
    return False


def serie_surveillee(texte):
    """
    Renvoie True si l'annonce concerne une série surveillée
    (ex : '151', 'Méga Évolution').
    """
    if not texte:
        return False
    texte_min = texte.lower()
    for serie in config.SERIES_SURVEILLEES:
        if serie.lower() in texte_min:
            return True
    return False


def annonce_valide(titre, description="", etat=""):
    """
    Vérifie tous les critères d'un coup.
    Renvoie (True, "ok") si l'annonce passe,
    sinon (False, "raison du rejet").
    On regarde le titre + la description ensemble.
    """
    texte_complet = f"{titre} {description}"

    # 1) Pas de lot/coffret/display...
    if contient_mot_interdit(texte_complet):
        return (False, "Contient un mot interdit (lot/coffret/display...)")

    # 2) Doit concerner une série surveillée
    if not serie_surveillee(texte_complet):
        return (False, "Série non surveillée")

    # 3) L'état doit être acceptable
    #    On regarde d'abord le champ 'etat', sinon le texte complet.
    if not (etat_accepte(etat) or etat_accepte(texte_complet)):
        return (False, "État non précisé ou non acceptable")

    return (True, "ok")
