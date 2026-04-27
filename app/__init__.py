from flask import Flask
from extensions import db
from app.routes import register_routes
from app.mechanics import mechanics_bp
from app.service_tickets import service_tickets_bp

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:Phoenix0350#@127.0.0.1:3306/mechanic_shop_db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    
    from models import Customer, Vehicle, ServiceTicket, Mechanic, ServiceMechanic
    
    with app.app_context():
        db.create_all()
        
    register_routes(app)
    app.register_blueprint(mechanics_bp, url_prefix="/mechanics")
    app.register_blueprint(service_tickets_bp, url_prefix="/service-tickets")
        
    return app