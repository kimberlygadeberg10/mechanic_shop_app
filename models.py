from extensions import db

class Customer(db.Model):
    __tablename__ = "customers"
    
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    vehicles = db.relationship("Vehicle", backref="customer")
    service_tickets = db.relationship("ServiceTicket", backref="customer")
    
class Vehicle(db.Model):
    __tablename__ = "vehicles"
    
    vehicle_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.customer_id"), nullable=False)
    vin = db.Column(db.String(17), unique=True, nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    license_plate = db.Column(db.String(20), nullable=False)
    color = db.Column(db.String(30))
    service_tickets = db.relationship("ServiceTicket", backref="vehicle")
    
class ServiceTicket(db.Model):
    __tablename__ ="service_tickets"
    
    ticket_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.customer_id"), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.vehicle_id"), nullable=False)
    date_opened = db.Column(db.Date, nullable=False)
    date_closed = db.Column(db.Date)
    service_description = db.Column(db.String(255), nullable=False)
    problem_reported = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    total_cost = db.Column(db.Numeric(10, 2), nullable=False)
    service_mechanics = db.relationship("ServiceMechanic", backref="service_ticket")
    mechanics = db.relationship("Mechanic", secondary="service_mechanics", back_populates="service_tickets")
    
class Mechanic(db.Model):
    __tablename__="mechanics"
    
    mechanic_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    salary = db.Column(db.Numeric(10, 2), nullable=False)
    service_mechanics = db.relationship("ServiceMechanic", backref="mechanic")
    service_tickets = db.relationship("ServiceTicket", secondary="service_mechanics", back_populates="mechanics")
    
class ServiceMechanic(db.Model):
    __tablename__="service_mechanics"
    
    ticket_id = db.Column(db.Integer, db.ForeignKey("service_tickets.ticket_id"), primary_key=True)
    mechanic_id = db.Column(db.Integer, db.ForeignKey("mechanics.mechanic_id"), primary_key=True)
    hours_worked = db.Column(db.Numeric(5, 2), nullable=True)
