from marshmallow import Schema, fields

class MechanicSchema(Schema):
    mechanic_id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    address = fields.Str(required=True)
    salary = fields.Decimal(required=True)