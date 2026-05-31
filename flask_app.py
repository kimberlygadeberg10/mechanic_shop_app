import os
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

# Import extensions
from extensions import db, ma, cache, limiter

# Import models so db.create_all() can create tables
from models import Mechanic, ServiceTicket, Inventory, ServiceMechanic

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
    CACHE_TYPE = "SimpleCache"


# Development configuration for local testing
class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+mysqlconnector://root:Phoenix0350%23@localhost/mechanic_shop_db"
    )
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "SimpleCache"


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
    # HOME / HEALTH CHECK ROUTE
    # ---------------------------------------------------------
    # This gives Render and users a simple page to confirm the API is live.

    @app.route("/")
    def home():
        return {
            "message": "Welcome to the Mechanic Shop API",
            "status": "deployed successfully",
            "documentation": "/api/docs"
        }, 200

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
    # CREATE DATABASE TABLES
    # ---------------------------------------------------------

    with app.app_context():
        db.create_all()

    return app


# Render/Gunicorn uses this app variable.
# Do not add app.run() for production deployment.
app = create_app(ProductionConfig)