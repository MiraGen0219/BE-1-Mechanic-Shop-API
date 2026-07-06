
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:FerretGarden2026!@localhost:3306/be1'
    DEBUG = True
    
class TestingConfig: 
    pass

class ProductionConfig:
    pass