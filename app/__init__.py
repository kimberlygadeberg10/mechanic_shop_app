from flask import Flask
from extensions import cache, db, limiter
from app.routes import register_routes
from app.mechanics import mechanics_bp
from app.service_tickets import service_tickets_bp

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:Phoenix0350#@127.0.0.1:3306/mechanic_shop_db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["CACHE_TYPE"] = "SimpleCache"
    app.config["CACHE_DEFAULT_TIMEOUT"] = 60
    
    db.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)
    
    from models import Customer, Vehicle, ServiceTicket, Mechanic, ServiceMechanic
    
    with app.app_context():
        db.create_all()
        
    register_routes(app)
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")
        
    return app
