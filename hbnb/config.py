"""Application configuration."""

import os
from datetime import timedelta
from collections.abc import Mapping


class Config:
    """Base configuration."""

    # Basic Flask config
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-change-this")
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///prod.db"

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key-change-this")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # Bcrypt
    BCRYPT_LOG_ROUNDS = 12


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"


class TestingConfig(Config):
    """Test configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"
    DEBUG = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)


# Config dictionary
config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
