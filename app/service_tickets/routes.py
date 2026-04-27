from flask import jsonify, request
from marshmallow import ValidationError

from extensions import db
from models import Mechanic, ServiceTicket
from app.service_tickets import service_tickets_bp
from app.service_tickets.schemas import ServiceTicketSchema


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)


@service_tickets_bp.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400


@service_tickets_bp.post("/")
def create_service_ticket():
    service_ticket_data = service_ticket_schema.load(request.get_json())
    new_service_ticket = ServiceTicket(**service_ticket_data)
    db.session.add(new_service_ticket)
    db.session.commit()
    return service_ticket_schema.dump(new_service_ticket), 201


@service_tickets_bp.put("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>")
def assign_mechanic(ticket_id, mechanic_id):
    service_ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    if mechanic not in service_ticket.mechanics:
        service_ticket.mechanics.append(mechanic)
        db.session.commit()

    return jsonify({"message": f"Mechanic {mechanic_id} assigned to ticket {ticket_id}."}), 200


@service_tickets_bp.put("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>")
def remove_mechanic(ticket_id, mechanic_id):
    service_ticket = ServiceTicket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)

    if mechanic in service_ticket.mechanics:
        service_ticket.mechanics.remove(mechanic)
        db.session.commit()

    return jsonify({"message": f"Mechanic {mechanic_id} removed from ticket {ticket_id}."}), 200


@service_tickets_bp.get("/")
def get_service_tickets():
    service_tickets = ServiceTicket.query.all()
    return service_tickets_schema.dump(service_tickets), 200
