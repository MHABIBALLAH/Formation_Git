"""
This module contains the configuration classes for the Flask application.
"""
import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_very_secret_key')
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://comptaaiadm:comptaaiadm@localhost:5432/comptaai"
    #SQLALCHEMY_DATABASE_URI ="sqlite:///E:/Formation_Git/ComptaAI/instance/comptaai.db"
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL',
    #    'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'instance', 'comptaai.db'))

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # Use in-memory DB for tests
    #SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://comptaaiadm:comptaaiadm@localhost:5432/comptaai"
    WTF_CSRF_ENABLED = False
