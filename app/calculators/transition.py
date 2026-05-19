from app.calculators.nouvelle import calculer_resultats_nouvelle
from app.calculators.shared import calcul_rendement

def calculer_resultats_transition(data):
    resultats_nouvelle = calculer_resultats_nouvelle(data)

    if not resultats_nouvelle:
        return {
            "energie_produite": 0,
            "incertitude_production": 0,
            "consommation_estimee": 0,
            "incertitude_consommation": 0,
            "rendement": 0,
            "incertitude_rendement": 0
        }

    conso_reelle = data.get("conso_maximale", 0)
    conso_estimee = resultats_nouvelle.get("consommation_estimee", 0)
    consommation_totale = conso_reelle

    rendement, incert_rendement = calcul_rendement(
        resultats_nouvelle.get("energie_produite", 0),
        consommation_totale
    )

    return {
        **resultats_nouvelle,
        "consommation_estimee": consommation_totale,
        "incertitude_consommation": resultats_nouvelle.get("incertitude_consommation", 0),
        "rendement": round(rendement * 100, 2),
        "incertitude_rendement": round(incert_rendement * 100, 2)
    }