import os
from apifairy import APIFairy
from flask import Flask, current_app
from dotenv import load_dotenv
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from supabase import create_client

# Load environment variables
load_dotenv()

# Initialize extensions
database = SQLAlchemy()
db_migration = Migrate()
ma = Marshmallow()
apifairy = APIFairy()

def create_app(config_type=os.getenv("CONFIG_TYPE")):
    # Create Flask app instance
    app = Flask(__name__)
    CORS(app)

    # Load configuration from environment or default
    app.config.from_object(config_type)

    # Check if Supabase URL and key are loaded
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL or SUPABASE_KEY not set in .env file")

    # Initialize the Supabase client
    app.config['SUPABASE_CLIENT'] = create_client(supabase_url, supabase_key)

    # Initialize the extensions
    initialize_extensions(app)

    # Register blueprints
    register_blueprint(app)
    
    return app

def initialize_extensions(app):
    # Initialize database, migration, marshmallow, apifairy
    database.init_app(app)
    db_migration.init_app(app, database)
    ma.init_app(app)
    apifairy.init_app(app)

    import core.models  # Import models after initializing extensions

def get_supabase():
    # Ensure current_app is available in the function context
    return current_app.config["SUPABASE_CLIENT"]

def register_blueprint(app):
    # Register blueprints for user API and file upload API
    from core.user_api import user_api_blueprint, file_upload_api_blueprint
    app.register_blueprint(user_api_blueprint, url_prefix="/api")
    app.register_blueprint(file_upload_api_blueprint, url_prefix="/api")
