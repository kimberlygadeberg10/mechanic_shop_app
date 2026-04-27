from flask import jsonify, request
from marshmallow import ValidationError

from extensions import db
from models import Mechanic
from app.mechanics import mechanics_bp
from app.mechanics.schemas import MechanicSchema


mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)


@mechanics_bp.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


@mechanics_bp.post("/")
def create_mechanic():
    mechanic_data = mechanic_schema.load(request.get_json())
    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    return mechanic_schema.dump(new_mechanic), 201


@mechanics_bp.get("/")
def get_mechanics():
    mechanics = Mechanic.query.all()
    return mechanics_schema.dump(mechanics), 200


@mechanics_bp.put("/<int:mechanic_id>")
def update_mechanic(mechanic_id):
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    mechanic_data = mechanic_schema.load(request.get_json(), partial=True)

    for field, value in mechanic_data.items():
        setattr(mechanic, field, value)

    db.session.commit()
    return mechanic_schema.dump(mechanic), 200


@mechanics_bp.delete("/<int:mechanic_id>")
def delete_mechanic(mechanic_id):
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": f"Mechanic {mechanic_id} deleted successfully."}), 200
