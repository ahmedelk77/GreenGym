def extraire_donnees_formulaire(form):
    """
    Extrait les données du formulaire en s'adaptant aux champs disponibles.
    Gère les trois profils : nouvelle, existante, transition.
    """
    data = {}

    try:
        if "surface_totale" in form:
            data["surface_totale"] = float(form.get("surface_totale", 0))
        if "surface_cardio" in form:
            data["surface_cardio"] = float(form.get("surface_cardio", 0))
        if "surface_piezo" in form:
            data["surface_piezo"] = float(form.get("surface_piezo", 0))
        if "nb_utilisateurs" in form:
            data["nb_utilisateurs"] = int(form.get("nb_utilisateurs", 0))
        if "heures_ouverture" in form:
            data["heures_ouverture"] = float(form.get("heures_ouverture", 0))
        if "jours_ouverture" in form:
            data["jours_ouverture"] = int(form.get("jours_ouverture", 0))
        if "conso_maximale" in form:
            data["conso_maximale"] = float(form.get("conso_maximale", 0))
        if "passages_par_jour" in form:
            data["passages_par_jour"] = float(form.get("passages_par_jour", 0))
    except Exception as e:
        print("❌ Erreur d'extraction des données :", e)

    return data
