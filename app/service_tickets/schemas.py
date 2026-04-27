from marshmallow import Schema, fields


class ServiceTicketSchema(Schema):
    ticket_id = fields.Int(dump_only=True)
    customer_id = fields.Int(required=True)
    vehicle_id = fields.Int(required=True)
    date_opened = fields.Date(required=True)
    date_closed = fields.Date(allow_none=True)
    service_description = fields.Str(required=True)
    problem_reported = fields.Str(required=True)
    status = fields.Str(required=True)
    total_cost = fields.Decimal(required=True)
