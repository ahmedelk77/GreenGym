# 📁 app/routes/__init__.py

from .routes_index import bp as bp_index
from .routes_nouvelle import bp as bp_nouvelle
from .routes_existante import bp as bp_existante
from .routes_transition import bp as bp_transition

__all__ = ["bp_index", "bp_nouvelle", "bp_existante", "bp_transition"]
