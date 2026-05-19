from flask import Blueprint, render_template, request, session
from app.utils.form_utils import extraire_donnees_formulaire
from app.calculators.transition import calculer_resultats_transition

bp = Blueprint("routes_transition", __name__, url_prefix="/form")

@bp.route("/transition", methods=["GET", "POST"])
def form_transition():
    if request.method == "POST":
        form_data = request.form
        data = extraire_donnees_formulaire(form_data)
        data["objectifs"] = session.get("objectifs", [])  # récupérer les objectifs
        results = calculer_resultats_transition(data)
        return render_template("public/resultats.html", results=results, profil="transition")
    
    return render_template("public/form_salle_transition.html")
