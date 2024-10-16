class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:sethmwebi@localhost:3308/author_manager_prod"
    )


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:sethmwebi@localhost:3308/author_manager_dev"
    )
    SQLACHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:sethmwebi@localhost:3308/author_manager_testing"
    )
    SQLACHEMY_ECHO = False
