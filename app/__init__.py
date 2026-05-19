import os
from flask import Flask
from sqlalchemy import create_engine
from app.models.shared import Base
from app.routes.routes_index import bp as bp_index

# ✅ Import des blueprints (routes modulaires)
from app.routes.routes_nouvelle import bp as bp_nouvelle
from app.routes.routes_existante import bp as bp_existante
from app.routes.routes_transition import bp as bp_transition

def init_database():
    """
    Initialise la base de données SQLite.
    Supprime l’ancienne base si elle n’est pas utilisée par un autre processus.
    """
    db_path = "green_gym.db"

    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print("🗑️ Ancienne base supprimée.")
        except PermissionError:
            print("❌ Impossible de supprimer la base : fichier utilisé par un autre processus.")
            return

    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    print("✅ Nouvelle base initialisée.")

def create_app():
    app = Flask(__name__)
    app.secret_key = "une_cle_secrete_tres_longue_et_complexe"

    # Initialisation conditionnelle de la BDD
    if os.environ.get("FLASK_RUN_FROM_CLI") != "true" and os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        init_database()

    # Enregistrement des routes par profil
    app.register_blueprint(bp_nouvelle)
    app.register_blueprint(bp_existante)
    app.register_blueprint(bp_transition)
    app.register_blueprint(bp_index)

    return app
