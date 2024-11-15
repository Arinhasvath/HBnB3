# app/__init__.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from prometheus_flask_exporter import PrometheusMetrics

# Initialisation des extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
metrics = PrometheusMetrics(app=None)

def create_app():
    """Fonction de création et de configuration de l'application Flask"""
    
    # Création de l'instance de l'application Flask
    app = Flask(__name__)
    
    # Configuration de l'application
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///hbnb.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialisation des extensions avec l'application
    db.init_app(app)
    bcrypt.init_app(app)
    metrics.init_app(app)
    
    # Importation et initialisation des modèles de base de données
    with app.app_context():
        from app.models import init_db
        init_db()
    
    # Définition des routes
    @app.route('/')
    @metrics.counter('hbnb_requests_total', 'Number of requests by endpoint')
    def main():
        return "Hello"
    
    return app
