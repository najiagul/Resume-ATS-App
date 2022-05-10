class Config(object):
    DEBUG = False
    TESTING = False
    ALLOWED_EXTENSIONS = ['txt', 'pdf', 'doc', 'docx']

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True