from flask import jsonify, request
from marshmallow import ValidationError

from extensions import db
from models import Customer, ServiceTicket
from schemas import CustomerSchema, LoginSchema
from auth import encode_token, token_required


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = LoginSchema()


def register_routes(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify(error.messages), 400

    @app.post("/customers")
    def create_customer():
        customer_data = customer_schema.load(request.get_json())
        new_customer = Customer(**customer_data)
        db.session.add(new_customer)
        db.session.commit()
        return customer_schema.dump(new_customer), 201
    
    @app.post("/login")
    def login():
        credentials = login_schema.load(request.get_json())
        
        customer = Customer.query.filter_by(email=credentials["email"]).first()
        
        if customer is None or customer.password != credentials["password"]:
            return jsonify({"message": "Invalid email or password."}), 401
        
        token = encode_token(customer.customer_id)
        return jsonify({"token": token}), 200
    
    @app.get("/my-tickets")
    @token_required
    def get_my_tickets(customer_id):
        tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()
        return jsonify([
            {
                "ticket_id": ticket.ticket_id,
                "customer_id": ticket.customer_id,
                "vehicle_id": ticket.vehicle_id,
                "date_opened": str(ticket.date_opened),
                "date_closed": str(ticket.date_closed) if ticket.date_closed else None,
                "service_description": ticket.service_description,
                "problem_reported": ticket.problem_reported,
                "status": ticket.status,
                "total_cost": str(ticket.total_cost)
            }
            for ticket in tickets
        ]), 200

    @app.get("/customers")
    def get_customers():
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)
        customers = Customer.query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            "customers": customers_schema.dump(customers.items),
            "total": customers.total,
            "pages": customers.pages,
            "current_page": customers.page
        }), 200

    @app.get("/customers/<int:customer_id>")
    def get_customer(customer_id):
        customer = Customer.query.get_or_404(customer_id)
        return customer_schema.dump(customer), 200

    @app.put("/customers/<int:customer_id>")
    @token_required
    def update_customer(auth_customer_id, customer_id):
        customer = Customer.query.get_or_404(customer_id)
        customer_data = customer_schema.load(request.get_json(), partial=True)

        for field, value in customer_data.items():
            setattr(customer, field, value)

        db.session.commit()
        return customer_schema.dump(customer), 200

    @app.delete("/customers/<int:customer_id>")
    @token_required
    def delete_customer(auth_customer_id, customer_id):
        customer = Customer.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": f"Customer {customer_id} deleted successfully."}), 200
