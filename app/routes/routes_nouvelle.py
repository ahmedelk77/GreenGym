from flask import Blueprint, render_template, request, session, redirect, url_for, make_response
from weasyprint import HTML
from app.utils.form_utils import extraire_donnees_formulaire
from app.calculators.nouvelle import calculer_resultats_nouvelle

bp = Blueprint("routes_nouvelle", __name__, url_prefix="/form")

# ✅ Étape 1 : Choix des objectifs
@bp.route("/nouvelle/objectif", methods=["GET", "POST"])
def form_objectif():
    if request.method == "POST":
        session["objectifs"] = request.form.getlist("objectifs")
        session["profil"] = session.get("profil", "nouvelle")
        return redirect(url_for("routes_nouvelle.form_configuration_spatiale"))

    session["profil"] = request.args.get("profil", "nouvelle")
    return render_template("public/form_objectif.html")


# ✅ Étape 2 : Configuration spatiale
@bp.route("/nouvelle/configuration", methods=["GET", "POST"])
def form_configuration_spatiale():
    if request.method == "POST":
        session["surface_totale"] = request.form.get("surface_totale")
        session["surface_cardio"] = request.form.get("surface_cardio")
        session["surface_piezo"] = request.form.get("surface_piezo")
        session["surface_dynamiques"] = request.form.get("surface_dynamiques")
        return redirect(url_for("routes_nouvelle.form_frequentation"))

    return render_template("public/form_configuration_spatiale.html")


# ✅ Étape 3 : Fréquentation & horaires
@bp.route("/nouvelle/frequentation", methods=["GET", "POST"])
def form_frequentation():
    if request.method == "POST":
        session["nb_adhérents"] = request.form.get("nb_adhérents")
        session["jours_ouverture"] = request.form.get("jours_ouverture")
        session["heures_ouverture"] = request.form.get("heures_ouverture")
        session["cours_collectifs"] = request.form.get("cours_collectifs", "non")
        return redirect(url_for("routes_nouvelle.form_machines_generatrices"))

    return render_template("public/form_frequentation.html")


# ✅ Étape 4 : Machines génératrices
@bp.route("/nouvelle/machines_generatrices", methods=["GET", "POST"])
def form_machines_generatrices():
    if request.method == "POST":
        # ✅ Machines standards
        session["nb_velos_generateurs"] = request.form.get("nb_velos_generateurs")
        session["nb_elliptiques_generateurs"] = request.form.get("nb_elliptiques_generateurs")
        session["nb_tapis_generateurs"] = request.form.get("nb_tapis_generateurs")

        # ✅ Machines personnalisées : liste de dictionnaires
        machines_perso = []
        noms = request.form.getlist("machine_perso_nom[]")
        nombres = request.form.getlist("machine_perso_nb[]")
        energies = request.form.getlist("machine_perso_energie[]")

        for nom, nb, energie in zip(noms, nombres, energies):
            try:
                nom_clean = nom.strip()
                nb_int = int(nb)
                energie_float = float(energie)

                if nom_clean and nb_int > 0 and energie_float >= 0:
                    machines_perso.append({
                        "nom": nom_clean,
                        "nombre": nb_int,
                        "energie_par_heure": energie_float
                    })
            except (ValueError, TypeError):
                continue  # Ignore les lignes invalides

        session["machines_personnalisees"] = machines_perso

        return redirect(url_for("routes_nouvelle.form_tarification"))

    return render_template("public/form_machines_generatrices.html")

# ✅ Étape 5 : Tarification électrique
@bp.route("/nouvelle/tarification", methods=["GET", "POST"])
def form_tarification():
    if request.method == "POST":
        session["type_tarif"] = request.form.get("type_tarif")
        session["devise"] = request.form.get("devise", "€")  # 🆕 ajout de la devise
        tarif_data = {}

        if session["type_tarif"] == "forfait":
            tarif_data["tarif_forfait"] = request.form.get("prix_annuel")

        elif session["type_tarif"] == "tranches":
            tranches = []
            tranches_tarifs = request.form.getlist("tranche_tarif[]")
            tranches_kWh = request.form.getlist("tranche_limite[]")
            for limite, tarif in zip(tranches_kWh, tranches_tarifs):
                try:
                    tranches.append({
                        "limite_kWh": float(limite),
                        "tarif": float(tarif)
                    })
                except ValueError:
                    continue
            tarif_data["tranches"] = tranches

        elif session["type_tarif"] == "heures":
            tarif_data["tarif_heures_pleines"] = request.form.get("tarif_hp")
            tarif_data["tarif_heures_creuses"] = request.form.get("tarif_hc")

        elif session["type_tarif"] == "abonnement":
            tarif_data["cout_abonnement_annuel"] = request.form.get("abonnement_annuel")
            tarif_data["tarif_conso"] = request.form.get("tarif_conso")

        session["tarif_data"] = tarif_data

        return redirect(url_for("routes_nouvelle.form_recapitulatif"))

    return render_template("public/form_tarification.html")



# ✅ Étape finale (temporaire, remplacera plus tard par page Résumé)
@bp.route("/nouvelle/recapitulatif", methods=["GET"])
def form_recapitulatif():
    # Rassemble toutes les données de session dans un seul dictionnaire propre
    data = {
        "objectifs": session.get("objectifs", []),
        "surface_totale": session.get("surface_totale", "Non renseigné"),
        "surface_cardio": session.get("surface_cardio", "Non renseigné"),
        "surface_piezo": session.get("surface_piezo", "Non renseigné"),
        "surface_dynamiques": session.get("surface_dynamiques", "Non renseigné"),
        "nb_adhérents": session.get("nb_adhérents", "Non renseigné"),
        "jours_ouverture": session.get("jours_ouverture", "Non renseigné"),
        "heures_ouverture": session.get("heures_ouverture", "Non renseigné"),
        "cours_collectifs": session.get("cours_collectifs", "non"),
        "nb_velos_generateurs": session.get("nb_velos_generateurs", "0"),
        "nb_elliptiques_generateurs": session.get("nb_elliptiques_generateurs", "0"),
        "nb_tapis_generateurs": session.get("nb_tapis_generateurs", "0"),
        "machines_personnalisees": session.get("machines_personnalisees", []),
        "type_tarif": session.get("type_tarif", "Non spécifié"),
        "tarif_data": session.get("tarif_data", {})
    }
    devise = session.get("devise", "€")

    return render_template("public/recapitulatif.html", data=data, devise=devise)


@bp.route("/nouvelle/resultats", methods=["GET"])
def resultats_nouvelle():
    data = {
        "objectifs": session.get("objectifs", []),
        "surface_totale": float(session.get("surface_totale", 0)),
        "surface_cardio": session.get("surface_cardio"),
        "surface_piezo": session.get("surface_piezo"),
        "surface_dynamiques": session.get("surface_dynamiques"),
        "nb_adhérents": int(session.get("nb_adhérents", 0)),
        "jours_ouverture": int(session.get("jours_ouverture", 0)),
        "heures_ouverture": int(session.get("heures_ouverture", 0)),
        "cours_collectifs": session.get("cours_collectifs"),
        "nb_velos_generateurs": int(session.get("nb_velos_generateurs", 0)),
        "nb_elliptiques_generateurs": int(session.get("nb_elliptiques_generateurs", 0)),
        "nb_tapis_generateurs": int(session.get("nb_tapis_generateurs", 0)),
        "machines_personnalisees": session.get("machines_personnalisees", []),
        "type_tarif": session.get("type_tarif"),
        "tarif_data": session.get("tarif_data", {}),
        "profil": "nouvelle"
    }

    results = calculer_resultats_nouvelle(data)
    devise = session.get("devise", "€")

    return render_template("public/resultats.html", data=data, results=results, profil="nouvelle", devise=devise)


@bp.route("/nouvelle/pdf", methods=["GET"])
def generer_pdf():
    try:
        data = {
            "objectifs": session.get("objectifs", []),
            "surface_totale": float(session.get("surface_totale", 0)),
            "surface_cardio": session.get("surface_cardio"),
            "surface_piezo": session.get("surface_piezo"),
            "surface_dynamiques": session.get("surface_dynamiques"),
            "nb_adhérents": int(session.get("nb_adhérents", 0)),
            "jours_ouverture": int(session.get("jours_ouverture", 0)),
            "heures_ouverture": int(session.get("heures_ouverture", 0)),
            "cours_collectifs": session.get("cours_collectifs"),
            "nb_velos_generateurs": int(session.get("nb_velos_generateurs", 0)),
            "nb_elliptiques_generateurs": int(session.get("nb_elliptiques_generateurs", 0)),
            "nb_tapis_generateurs": int(session.get("nb_tapis_generateurs", 0)),
            "machines_personnalisees": session.get("machines_personnalisees", []),
            "type_tarif": session.get("type_tarif"),
            "tarif_data": session.get("tarif_data", {})
        }

        results = calculer_resultats_nouvelle(data)
        devise = session.get("devise", "€")

        rendered = render_template("public/rapport_pdf.html", data=data, results=results, devise=devise)
        pdf = HTML(string=rendered).write_pdf()

        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=rapport_energie.pdf"
        return response

    except Exception as e:
        return f"Erreur lors de la génération du PDF : {e}", 500

@bp.route("/nouvelle/pdf_recapitulatif", methods=["GET"])
def generer_pdf_recapitulatif():
    try:
        data = {
            "objectifs": session.get("objectifs", []),
            "surface_totale": session.get("surface_totale"),
            "surface_cardio": session.get("surface_cardio"),
            "surface_piezo": session.get("surface_piezo"),
            "surface_dynamiques": session.get("surface_dynamiques"),
            "nb_adhérents": session.get("nb_adhérents"),
            "jours_ouverture": session.get("jours_ouverture"),
            "heures_ouverture": session.get("heures_ouverture"),
            "cours_collectifs": session.get("cours_collectifs"),
            "nb_velos_generateurs": session.get("nb_velos_generateurs"),
            "nb_elliptiques_generateurs": session.get("nb_elliptiques_generateurs"),
            "nb_tapis_generateurs": session.get("nb_tapis_generateurs"),
            "machines_personnalisees": session.get("machines_personnalisees", []),
            "type_tarif": session.get("type_tarif"),
            "tarif_data": session.get("tarif_data", {})
        }
        devise = session.get("devise", "€")
        rendered = render_template("public/rapport_recapitulatif.html", data=data, devise=devise)
        pdf = HTML(string=rendered).write_pdf()
        response = make_response(pdf)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=recapitulatif_projet.pdf"
        return response

    except Exception as e:
        return f"Erreur PDF : {e}", 500
