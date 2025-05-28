class Config:
    SQLALCHEMY_DATABASE_URI = "xxxxxx"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    DEBUG = True
    PROPAGATE_EXCEPTIONS = True

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    DEBUG = False
