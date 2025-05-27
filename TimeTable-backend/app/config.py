class Config:
    SQLALCHEMY_DATABASE_URI = "xxxxxxxx"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    DEBUG = True

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    DEBUG = False
