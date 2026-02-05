"""Configuration management for Surakshita"""
import os
import secrets
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # Security: Load from environment or generate warning
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        print("WARNING: SECRET_KEY not set in environment! Using generated key (not recommended for production)")
        SECRET_KEY = secrets.token_hex(32)
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True') == 'True'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = int(os.getenv('SESSION_TIMEOUT', 1800))
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')
    
    # WTF CSRF
    WTF_CSRF_TIME_LIMIT = None  # No timeout for CSRF tokens


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # Allow HTTP in dev


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # Force HTTPS
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing
    SESSION_COOKIE_SECURE = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
