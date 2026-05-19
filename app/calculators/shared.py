import math

# -----------------------------
# 📁 calculator.py — Calculs énergétiques et incertitudes
# -----------------------------

# 🧠 Pourquoi cette méthode d’estimation d’incertitude ?
#
# Dans notre application, nous estimons plusieurs grandeurs physiques (énergie produite,
# consommation d’éclairage, rendement énergétique...), toutes dépendant de **multiples variables** 
# mesurées ou estimées par l’utilisateur.
#
# Pour évaluer rigoureusement l’incertitude associée à ces calculs, nous utilisons la méthode 
# de **propagation des incertitudes par dérivation quadratique**, également connue sous le nom 
# de **formule de Gauss** :
#
#     ΔY ≈ Y × sqrt( (u(x₁)/x₁)² + (u(x₂)/x₂)² + ... )
#
# ✅ Cette méthode est idéale lorsque :
#   ▪️ La grandeur d’intérêt (Y) est une fonction **multiplicative** de plusieurs variables,
#   ▪️ Les variables sont **indépendantes** les unes des autres,
#   ▪️ Leurs **incertitudes relatives sont modérées** (typiquement < 30%).
#
# 📖 Référence : Guide to the Expression of Uncertainty in Measurement (GUM),
# document de référence international en évaluation d’incertitudes.


import math

def calcul_energie_piezo_et_incertitude(nb_pas_total_utilisateur, surface_piezo, surface_totale,
                                           nb_utilisateurs_par_jour, nb_jours_ouverture,
                                           energie_par_pas, u_pas_total, u_surface):
    """
    Calcule l'énergie produite par les dalles piézoélectriques en kWh et son incertitude.

    📌 Hypothèses :
    - L'énergie générée est proportionnelle à la surface piézo par rapport à la surface totale.
    - L’énergie produite dépend du nombre de pas dynamiques (pondérés par la surface utile).

    Formule :
        E = nb_pas × (surface_piezo / surface_totale) × nb_utilisateurs × nb_jours × énergie_par_pas / 1000
    """

    proportion_zone_dyn = surface_piezo / surface_totale
    nb_pas_dyn = nb_pas_total_utilisateur * proportion_zone_dyn
    energie_wh = nb_pas_dyn * nb_utilisateurs_par_jour * nb_jours_ouverture * energie_par_pas
    energie_kwh = energie_wh / 1000

    # Propagation de l’incertitude selon Gauss
    u_relative = math.sqrt(u_pas_total**2 + u_surface**2)
    incertitude_kwh = energie_kwh * u_relative

    return round(energie_kwh, 2), round(incertitude_kwh, 2)




def cout_electricite_forfait(total_kwh, tarif_kwh):
    """
    Calcule le coût électrique total selon un tarif fixe (forfaitaire).
    Exemple : 0,18 €/kWh.
    """
    return round(total_kwh * tarif_kwh, 2)


def cout_electricite_tranches(total_kwh, tranches):
    """
    Calcule le coût total selon une tarification par tranches.

    Exemple de tranches : [(100, 0.15), (200, 0.18), (float('inf'), 0.20)]
    → Les premiers 100 kWh à 0.15€, les 200 suivants à 0.18€, le reste à 0.20€.
    """
    cout = 0
    kwh_restant = total_kwh
    for limite, tarif in tranches:
        if kwh_restant > limite:
            cout += limite * tarif
            kwh_restant -= limite
        else:
            cout += kwh_restant * tarif
            break
    return round(cout, 2)


def calcul_rendement(energie_produite, consommation_totale, u_prod=0.10, u_conso=0.05):
    """
    Calcule le rendement énergétique global : η = E_prod / E_conso

    📌 Hypothèses :
    - Incertitude relative sur E_prod : 10% (issue des pas, comportement, rendement dalle)
    - Incertitude relative sur E_conso : 5% (conso éclairage mieux maîtrisée)

    Formule d’incertitude (propagation quadratique) :
        ∆η ≈ η × sqrt( (u(Ep)/Ep)^2 + (u(Ec)/Ec)^2 )
    """
    eta = energie_produite / consommation_totale if consommation_totale else 0
    incertitude = eta * math.sqrt(u_prod**2 + u_conso**2) if consommation_totale else 0
    return round(eta, 4), round(incertitude, 4)

def calcul_incertitude_machine_generatrice():
    """
    📐 Calcule l'incertitude relative pour l'énergie produite par une machine génératrice,
    selon la formule de propagation quadratique (formule de Gauss).

    Hypothèses (voir justification scientifique) :
    - Puissance machine : ±15%
    - Durée d'utilisation : ±10%
    - Nombre d'utilisateurs : ±10%
    - Jours d'ouverture : ±5%
    - Nombre de machines : 0% (connu avec certitude)

    🔁 Formule :
        ΔE/E = √( (ΔP/P)² + (Δt/t)² + (ΔU/U)² + (ΔJ/J)² )
    """
    return math.sqrt(0.15**2 + 0.10**2 + 0.10**2 + 0.05**2)  # ≈ 0.21


def calcul_energie_machines_generatrices(nb_jours, nb_utilisateurs, duree_moyenne, 
                                          nb_velos=0, nb_elliptiques=0, nb_tapis=0,
                                          machines_personnalisees=[]):
    """
    ⚙️ Calcule l'énergie produite par toutes les machines génératrices (standard + personnalisées)

    Paramètres :
    - nb_jours : nombre de jours d'ouverture/an
    - nb_utilisateurs : utilisateurs/jour
    - duree_moyenne : durée moyenne d'utilisation (en heures)
    - nb_velos, nb_elliptiques, nb_tapis : nombre de machines standards
    - machines_personnalisees : liste de dicts {"nom": ..., "nombre": ..., "energie_par_heure": ...}

    Valeurs standard utilisées :
    - Vélo : 100 Wh/h
    - Elliptique : 100 Wh/h
    - Tapis : 200 Wh/h
    """

    # 🔋 Puissances moyennes (en Wh/h) — sources : SportsArt, ReRev, Precor
    P_VELO = 100
    P_ELLIPTIQUE = 100
    P_TAPIS = 200

    # 🔢 Calcul énergie par type de machine
    E_velos = nb_velos * P_VELO * duree_moyenne * nb_utilisateurs * nb_jours
    E_elliptiques = nb_elliptiques * P_ELLIPTIQUE * duree_moyenne * nb_utilisateurs * nb_jours
    E_tapis = nb_tapis * P_TAPIS * duree_moyenne * nb_utilisateurs * nb_jours

    # 🔧 Machines personnalisées
    E_perso = 0
    for m in machines_personnalisees:
        nombre = m.get("nombre", 0)
        energie_h = m.get("energie_par_heure", 0)
        E_perso += nombre * energie_h * duree_moyenne * nb_utilisateurs * nb_jours

    # ⚡ Total énergie produite (en Wh → kWh)
    E_total_Wh = E_velos + E_elliptiques + E_tapis + E_perso
    E_total_kWh = E_total_Wh / 1000

    # 📐 Incertitude sur cette énergie
    u_rel = calcul_incertitude_machine_generatrice()
    u_kWh = E_total_kWh * u_rel

    return round(E_total_kWh, 2), round(u_kWh, 2)

def calcul_consommation_globale(surface_totale, heures_par_jour, jours_ouverture_par_semaine, 
                                 puissance_moyenne_w_m2=30,
                                 u_surface=0.05, u_heures=0.05, u_jours=0.05, u_puissance=0.10):
    """
    ⚡ Calcule la consommation annuelle totale d'énergie en kWh pour la salle.

    🔢 Formule utilisée :
    E = S × P × h × j / 1000
    où :
      - S : surface totale (m²)
      - P : puissance moyenne absorbée (W/m²)
      - h : heures/jour d'ouverture
      - j : jours d'ouverture/an = jours/semaine × 52

    📉 Incertitude (ΔE) :
    ΔE ≈ E × sqrt( (u_S/S)² + (u_P/P)² + (u_h/h)² + (u_j/j)² )

    🧠 Hypothèses :
    - u_surface = ±5% (marge sur estimation plans ou surfaces éclairées réelles)
    - u_heures = ±5% (variations de durée d’éclairage ou fonctionnement des équipements)
    - u_jours  = ±5% (vacances, fermetures imprévues)
    - u_puissance = ±10% (variation selon équipements, usage réel, ventilation…)

    📌 Source puissance : ADEME, RT2012 Gymnases – estimée entre 20-40 W/m² → 30 W/m² est réaliste.
    """
    jours_par_an = jours_ouverture_par_semaine * 52
    E = surface_totale * puissance_moyenne_w_m2 * heures_par_jour * jours_par_an / 1000

    # Formule de propagation quadratique
    u_relative = math.sqrt(
        u_surface**2 + 
        u_puissance**2 +
        u_heures**2 +
        u_jours**2
    )
    incertitude = E * u_relative

    return round(E, 2), round(incertitude, 2)

def estimer_nb_utilisateurs_par_jour(nb_adhérents, jours_ouverture_par_semaine, frequence_hebdo=2.5):
    """
    Estime le nombre moyen d’utilisateurs quotidiens à partir du nombre d’adhérents.

    Formule :
    nb_journalier = (adhérents × fréquence hebdomadaire) / jours d’ouverture
    """
    if jours_ouverture_par_semaine == 0:
        return 0
    return round((nb_adhérents * frequence_hebdo) / jours_ouverture_par_semaine)

def calculer_cout_energetique(data, energie_produite, energie_consomme):
    """
    💶 Calcule le coût énergétique total, le coût économisé, le reste à payer et le taux de couverture.
    ✔ Gère les types de tarification : forfait fixe, par tranches, heures pleines/creuses, abonnement + conso.

    📥 Entrées :
    - data : dictionnaire contenant les clés 'type_tarif' et 'tarif_data'
    - energie_produite : énergie produite annuelle (en kWh)
    - energie_consomme : énergie consommée annuelle (en kWh)

    📤 Sorties :
    - cout_total : coût théorique sans énergie produite
    - cout_economise : part du coût évitée grâce à la production
    - cout_restant : ce qu’il faut encore payer
    - taux_couverture : (énergie produite / consommée) × 100
    """

    type_tarif = data.get("type_tarif", "")
    tarif_data = data.get("tarif_data", {})

    cout_total = 0
    cout_economise = 0

    energie_utilisee = min(energie_produite, energie_consomme)

    # ▫️ Type 1 : Forfait fixe
    if type_tarif == "forfait":
        cout_total = float(tarif_data.get("tarif_forfait", 0))
        cout_economise = cout_total if energie_produite >= energie_consomme else cout_total * (energie_produite / energie_consomme)

    # ▫️ Type 2 : Par tranches
    elif type_tarif == "tranches":
        tranches = tarif_data.get("tranches", [])
        tranches = sorted(tranches, key=lambda x: x["limite_kWh"])
        restant = energie_consomme
        restant_prod = energie_utilisee
        prev_limite = 0

        for tranche in tranches:
            limite = tranche["limite_kWh"]
            tarif = tranche["tarif"]

            quantite = min(limite - prev_limite, restant)
            cout_total += quantite * tarif

            if restant_prod > 0:
                prod_qte = min(quantite, restant_prod)
                cout_economise += prod_qte * tarif
                restant_prod -= prod_qte

            restant -= quantite
            prev_limite = limite

            if restant <= 0:
                break

        # Dernière tranche illimitée
        if restant > 0:
            tarif_final = tranches[-1]["tarif"]
            cout_total += restant * tarif_final
            if restant_prod > 0:
                cout_economise += min(restant, restant_prod) * tarif_final

    # ▫️ Type 3 : Heures pleines / creuses
    elif type_tarif == "heures":
        hp = float(tarif_data.get("tarif_heures_pleines", 0))
        hc = float(tarif_data.get("tarif_heures_creuses", 0))
        ratio_hp, ratio_hc = 0.6, 0.4

        E_hp = energie_consomme * ratio_hp
        E_hc = energie_consomme * ratio_hc

        cout_total = E_hp * hp + E_hc * hc

        E_prod_hp = energie_utilisee * ratio_hp
        E_prod_hc = energie_utilisee * ratio_hc

        cout_economise = E_prod_hp * hp + E_prod_hc * hc
    # ▫️ Type 4 : Abonnement + consommation
    elif type_tarif == "abonnement":
        abonnement = float(tarif_data.get("abonnement_annuel", 0))
        tarif = float(tarif_data.get("tarif_conso", 0))

        cout_total = abonnement + (energie_consomme * tarif)
        cout_economise = min(energie_utilisee, energie_consomme) * tarif  # l'abonnement est fixe

    # Valeurs finales
    cout_total = round(cout_total, 2)
    cout_economise = round(cout_economise, 2)
    cout_restant = round(max(cout_total - cout_economise, 0), 2)
    taux_couverture = round((energie_produite / energie_consomme) * 100, 2) if energie_consomme > 0 else 0

    return {
        "cout_total": cout_total,
        "cout_economise": cout_economise,
        "cout_a_payer": cout_restant,
        "taux_couverture": taux_couverture
    }

