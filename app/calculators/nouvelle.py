import math
from app.calculators.shared import (
    calcul_energie_piezo_et_incertitude,
    calcul_energie_machines_generatrices,
    calcul_rendement,
    calcul_consommation_globale,
    estimer_nb_utilisateurs_par_jour,
    calculer_cout_energetique
)

def calculer_resultats_nouvelle(data):
    # 🔹 1. Données utilisateur
    nb_adhérents = int(data.get("nb_adhérents", 300))
    jours_ouverture_semaine = int(data.get("jours_ouverture", 6))
    nb_jours_ouverture = jours_ouverture_semaine * 52
    nb_utilisateurs = estimer_nb_utilisateurs_par_jour(nb_adhérents, jours_ouverture_semaine)

    duree_moyenne_h = 1.25
    proportion_zone_dyn = 0.6

    nb_velos = int(data.get("nb_velos_generateurs", 0))
    nb_elliptiques = int(data.get("nb_elliptiques_generateurs", 0))
    nb_tapis = int(data.get("nb_tapis_generateurs", 0))
    machines_perso = data.get("machines_personnalisees", [])

    surface_totale = float(data.get("surface_totale", 100))
    heures_ouverture = float(data.get("heures_ouverture", 10))
    surface_piezo = float(data.get("surface_piezo", 10))

    # 🔹 2. Énergie piézo
    E_piezo, u_piezo = calcul_energie_piezo_et_incertitude(
        nb_pas_total_utilisateur=6250,
        surface_piezo=surface_piezo,
        surface_totale=surface_totale,
        nb_utilisateurs_par_jour=nb_utilisateurs,
        nb_jours_ouverture=nb_jours_ouverture,
        energie_par_pas=0.05,
        u_pas_total=0.10,
        u_surface=0.15
    )

    # 🔹 3. Énergie générée par les machines
    E_machines, u_machines = calcul_energie_machines_generatrices(
        nb_jours=nb_jours_ouverture,
        nb_utilisateurs=nb_utilisateurs,
        duree_moyenne=duree_moyenne_h,
        nb_velos=nb_velos,
        nb_elliptiques=nb_elliptiques,
        nb_tapis=nb_tapis,
        machines_personnalisees=machines_perso
    )

    # 🔹 4. Énergie totale produite
    energie_totale = E_piezo + E_machines
    if E_piezo > 0 and E_machines > 0:
        u_relative = math.sqrt((u_piezo / E_piezo) ** 2 + (u_machines / E_machines) ** 2)
        incertitude_totale = round(energie_totale * u_relative, 2)
    else:
        incertitude_totale = round(u_piezo + u_machines, 2)

    # 🔹 5. Consommation estimée
    E_conso, u_conso = calcul_consommation_globale(
        surface_totale=surface_totale,
        heures_par_jour=heures_ouverture,
        jours_ouverture_par_semaine=jours_ouverture_semaine
    )

    # 🔹 6. Rendement global
    rendement, incert_rendement = calcul_rendement(
        energie_totale,
        E_conso,
        u_prod=(incertitude_totale / energie_totale) if energie_totale else 0.1,
        u_conso=(u_conso / E_conso) if E_conso else 0.05
    )

    # 🔹 7. Coûts énergétiques
    couts = calculer_cout_energetique(data, energie_produite=energie_totale, energie_consomme=E_conso)


    # 🔹 8. Génération du commentaire personnalisé
    commentaire = generer_commentaire(
        rendement=rendement * 100,
        energie_piezo=E_piezo,
        energie_machines=E_machines
    )

    return {
        "energie_piezo": round(E_piezo, 2),
        "energie_machines": round(E_machines, 2),
        "energie_produite": round(energie_totale, 2),
        "incertitude_production": incertitude_totale,
        "consommation_estimee": round(E_conso, 2),
        "incertitude_consommation": round(u_conso, 2),
        "rendement": round(rendement * 100, 2),
        "incertitude_rendement": round(incert_rendement * 100, 2),
        "cout_annuel": couts["cout_total"],
        "cout_economise": couts["cout_economise"],
        "cout_restant": couts["cout_a_payer"],
        "taux_couverture": couts["taux_couverture"],
        "commentaire": commentaire
    }

def generer_commentaire(energie_piezo, energie_machines, rendement):
    commentaire = ""
    total = energie_piezo + energie_machines
    if total == 0:
        commentaire = "Aucune énergie produite. Vérifiez vos paramètres de configuration."
        return commentaire

    pct_piezo = energie_piezo / total * 100
    pct_machines = energie_machines / total * 100

    if rendement < 30:
        if pct_piezo < 10:
            commentaire = "🔧 Le rendement est très faible. Envisagez d’augmenter la surface piézoélectrique pour capter davantage d’énergie de passage."
        elif pct_machines < 50:
            commentaire = "🔧 Le rendement est très faible. Pensez à installer plus de machines génératrices ou optimiser leur usage."
        else:
            commentaire = "🔍 Le rendement est faible malgré une bonne contribution des équipements. Reconsidérez les heures d’ouverture ou le comportement des utilisateurs."

    elif rendement < 60:
        if pct_piezo < 10:
            commentaire = "📉 Le rendement reste modéré. Une meilleure exploitation de la zone piézoélectrique pourrait améliorer les performances."
        elif pct_machines < 50:
            commentaire = "📉 Le rendement reste modéré. Augmenter le nombre ou la puissance des machines pourrait être bénéfique."
        else:
            commentaire = "📈 Rendement modéré. Optimisez l’occupation de la salle pour améliorer encore l’efficacité énergétique."

    elif rendement < 99:
        if pct_piezo < 10:
            commentaire = "👍 Bon rendement, mais la contribution des dalles piézo est faible. Un petit ajout pourrait rendre la salle encore plus autonome."
        elif pct_machines < 50:
            commentaire = "👍 Bon rendement, mais les machines pourraient encore contribuer davantage. Évaluez leur positionnement ou fréquence d’utilisation."
        else:
            commentaire = "✅ Très bon rendement. Vos équipements sont bien dimensionnés."

    else:
        commentaire = "🌟 Excellent ! Votre salle est 100% autonome ou plus. Vous pourriez même revendre votre surplus d’énergie !"

    return commentaire


