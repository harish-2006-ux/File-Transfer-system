"""
VaultX Configuration Settings
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # Upload
    UPLOAD_FOLDER = 'storage/encrypted_files'
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 10 * 1024 * 1024))  # 10MB
    
    # Encryption
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
    
    # Email
    SENDER_EMAIL = os.getenv('SENDER_EMAIL', 'noreply@vaultx.com')
    SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
    
    # Database
    DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'supabase')
    
    # Supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = 'memory://'
    
    # Session
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    RATELIMIT_STORAGE_URL = 'redis://localhost:6379'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    DATABASE_TYPE = 'sqlite'
