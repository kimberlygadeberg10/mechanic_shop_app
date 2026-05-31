import os
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

# Import extensions
from extensions import db, ma, cache, limiter

# Import models so SQLAlchemy can create the tables
from models import Mechanic, ServiceTicket, Inventory

# Import blueprints
from app.mechanics import mechanics_bp
from app.inventory import inventory_bp
from app.service_tickets import service_tickets_bp


# Production configuration for Render
class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+mysqlconnector://root:Phoenix0350%23@localhost/mechanic_shop_db"
    )
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Development configuration for running locally
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+mysqlconnector://root:Phoenix0350%23@localhost/mechanic_shop_db"
    )
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)

    # ---------------------------------------------------------
    # SWAGGER CONFIGURATION
    # ---------------------------------------------------------

    SWAGGER_URL = "/api/docs"
    API_URL = "/static/swagger.json"

    swagger_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            "app_name": "Mechanic Shop API"
        }
    )

    app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

    # ---------------------------------------------------------
    # REGISTER BLUEPRINTS
    # ---------------------------------------------------------

    app.register_blueprint(mechanics_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(service_tickets_bp)

    # ---------------------------------------------------------
    # HOME ROUTE
    # ---------------------------------------------------------

    @app.route("/")
    def home():
        return {
            "message": "Welcome to the Mechanic Shop API"
        }

    # ---------------------------------------------------------
    # CREATE DATABASE TABLES
    # ---------------------------------------------------------

    with app.app_context():
        db.create_all()

    return app


# Render/Gunicorn uses this app variable.
# Do not use app.run() for production deployment.
app = create_app(ProductionConfig)