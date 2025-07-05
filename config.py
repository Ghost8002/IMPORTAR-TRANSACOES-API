import os

class Config:
    """Configuração base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'ofx'}

class DevelopmentConfig(Config):
    """Configuração para desenvolvimento"""
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000

class ProductionConfig(Config):
    """Configuração para produção"""
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = int(os.environ.get('PORT', 5000))
    
    # Configurações de segurança
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # CORS - Configure para seu domínio
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Rate limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = "memory://"

class TestingConfig(Config):
    """Configuração para testes"""
    TESTING = True
    DEBUG = True

# Mapeamento de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 