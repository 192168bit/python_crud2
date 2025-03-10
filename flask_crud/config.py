import os
from sqlalchemy.engine.url import URL

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config():
    SECRET_KEY = os.getenv("SECRET_KEY")
    FLASK_ENV = os.getenv("FLASK_ENV")
    DEBUG = os.getenv("DEBUG")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")

class DevelopmentConfig():
    DEBUG = True
    
    url_object = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME")
    )
    
    SQLALCHEMY_DATABASE_URI = url_object
    
    APIFAIRY_TITLE = 'Sample_CRUD'
    APIFAIRY_UI = 'swagger_ui'
    APIFAIRY_VERSION = 1.0

class ProductionConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False