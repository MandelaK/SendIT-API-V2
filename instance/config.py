import os

class Config():
    """Main configuration class"""
    DEBUG = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

class Development(Config):
    """Configuration for development"""
    DEBUG = True
    DATABASE_URL = os.getenv('DATABASE_URL')

class Testing(Config):
    """Configuration for testing"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = os.getenv('DATABASE_TEST_URL')

class Production(Config):
    """Configuration for production"""
    DEBUG = False
    DATABASE_URL = os.getenv('DATABASE_PRODUCTION_URL')

app_config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
    'default': Development
}
