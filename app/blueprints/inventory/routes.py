from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import db, Inventory
from app.blueprints.inventory import inventory_bp
from app.blueprints.inventory.schemas import inventory_schema, inventories_schema


#CREATE / POST INVENTORY
@inventory_bp.route("/", methods=['POST'])
def create_inventory_item():
    
    try:
        item_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_item = Inventory(**item_data)
    
    db.session.add(new_item)
    db.session.commit()
    
    return inventory_schema.jsonify(new_item), 201

#GET ALL INVENTORY
@inventory_bp.route("/", methods=['GET'])
def get_inventory():
    query = select(Inventory)
    inventory = db.session.execute(query).scalars().all()
    
    return inventories_schema.jsonify(inventory), 200

#GET INVENTORY BY ID
@inventory_bp.route("/<int:item_id>", methods=['GET'])
def get_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)
    
    if not item:
        return jsonify({"error": "Inventory item not found"}), 404
    
    return inventory_schema.jsonify(item), 200

#EDIT / PUT INVENTORY BY ID
@inventory_bp.route("/<int:item_id>", methods=['PUT'])
def update_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)
    
    if not item: 
        return jsonify({"error": "Inventory item not found"}), 404
    
    try:
        item_data = inventory_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in item_data.items():
        setattr(item, key, value)
        
    db.session.commit()
        
    return inventory_schema.jsonify(item), 200

#DELETE INVENTORY
@inventory_bp.route("/<int:item_id>", methods=['DELETE'])
def delete_inventory_item(item_id):
    item = db.session.get(Inventory, item_id)
    
    if not item:
        return jsonify({"error": "Inventory item not found"}), 404
    
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({"message": f"Inventory item {item_id} deleted successfully"}), 200