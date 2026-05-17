from flask import jsonify, request
from marshmallow import ValidationError

from extensions import db
from models import Inventory
from app.inventory import inventory_bp
from app.inventory.schemas import InventorySchema


inventory_schema = InventorySchema()
inventory_items_schema = InventorySchema(many=True)

@inventory_bp.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify(error.messages), 400

@inventory_bp.post("/")
def create_inventory_item():
    inventory_data = inventory_schema.load(request.get_json())
    new_inventory_item = Inventory(**inventory_data)
    db.session.add(new_inventory_item)
    db.session.commit()
    return inventory_schema.dump(new_inventory_item), 201

@inventory_bp.get("/")
def get_inventory_items():
    inventory_items = Inventory.query.all()
    return inventory_items_schema.dump(inventory_items), 200

@inventory_bp.put("/<int:inventory_id>")
def update_inventory_item(inventory_id):
    inventory_item = Inventory.query.get_or_404(inventory_id)
    inventory_data = inventory_schema.load(request.get_json(), partial=True)
    
    for field, value in inventory_data.items():
        setattr(inventory_item, field, value)
        
    db.session.commit()
    return inventory_schema.dump(inventory_item), 200

@inventory_bp.delete("/<int:inventory_id>")
def delete_inventory_item(inventory_id):
    inventory_item = Inventory.query.get_or_404(inventory_id)
    db.session.delete(inventory_item)
    db.session.commit()
    return jsonify({"message": f"Inventory item {inventory_id} deleted successfully."}), 200