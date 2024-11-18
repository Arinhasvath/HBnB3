# app/__init__.py
"""Main application module"""
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from prometheus_flask_exporter import PrometheusMetrics
from app.db import db

# Initialisation des extensions
bcrypt = Bcrypt()
migrate = Migrate()
metrics = PrometheusMetrics(app=None)


def create_app(config_name="default"):
    """
    Factory pattern pour créer l'application Flask
    Args:
        config_name: Configuration à utiliser ('default', 'testing', etc.)
    """
    app = Flask(__name__)

    # Configuration
    if config_name == "testing":
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["TESTING"] = True
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hbnb.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "dev"  # À changer en production

    # Initialisation des extensions
    db.init_app(app)
    bcrypt.init_app(app)
    metrics.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        # Import des modèles
        from app.models.user import User
        from app.models.place import Place
        from app.models.review import Review
        from app.models.amenity import Amenity

        # Création des tables
        db.create_all()

    return app
