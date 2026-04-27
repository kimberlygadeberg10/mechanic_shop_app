from flask import jsonify, request
from marshmallow import ValidationError

from extensions import db
from models import Customer
from schemas import CustomerSchema


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


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

    @app.get("/customers")
    def get_customers():
        customers = Customer.query.all()
        return customers_schema.dump(customers), 200

    @app.get("/customers/<int:customer_id>")
    def get_customer(customer_id):
        customer = Customer.query.get_or_404(customer_id)
        return customer_schema.dump(customer), 200

    @app.put("/customers/<int:customer_id>")
    def update_customer(customer_id):
        customer = Customer.query.get_or_404(customer_id)
        customer_data = customer_schema.load(request.get_json(), partial=True)

        for field, value in customer_data.items():
            setattr(customer, field, value)

        db.session.commit()
        return customer_schema.dump(customer), 200

    @app.delete("/customers/<int:customer_id>")
    def delete_customer(customer_id):
        customer = Customer.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": f"Customer {customer_id} deleted successfully."}), 200
