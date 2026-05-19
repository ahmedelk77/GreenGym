from flask import Blueprint, render_template

bp = Blueprint("routes_index", __name__)

@bp.route("/")
def index():
    return render_template("public/index.html")
