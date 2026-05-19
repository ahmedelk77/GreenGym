import os
from sqlalchemy import create_engine

# ✅ Import des modèles partagés (Base + classes si besoin)
from app.models.shared import Base

def init_database():
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

if __name__ == "__main__":
    init_database()
