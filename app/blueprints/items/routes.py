from .schemas import item_schema, items_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import Item, db
from . import items_bp
from app.extensions import limiter, cache


#CREATE ITEM
@items_bp.route('/', methods=['POST'])
def create_item():
    try: 
        item_data = item_schema.load(request.json)
    except ValidationError as e: 
        return jsonify(e.messages), 400
    
    new_item = Item(item_name=item_data['item_name'], price=item_data['price'])
    
    db.session.add(new_item)
    db.session.commit()
    
    return item_schema.jsonify(new_item), 201

#GET ALL ITEMS
@items_bp.route('/', methods=['GET'])
@cache.cached(timeout=60)
def get_items(): 
    query = select(Item)
    result = db.session.execute(query).scalars().all()
    
    return items_schema.jsonify(result), 200
    
#GET ITEM BY ID
@items_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = db.session.get(Item, item_id)
    
    if item: 
        return item_schema.jsonify(item), 200
    else:
        return jsonify({"error": "Item not found."}), 404
    
#UPDATE ITEM
@items_bp.route('/<int:item_id>', methods=['PUT'])
@limiter.limit("5 per day")
def update_item(item_id): 
    item = db.session.get(Item, item_id)
    
    if not item: 
        return jsonify({"error": "Item not found."}), 404
    
    try:
        item_data = item_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in item_data.items():
        setattr(item, field, value)

    db.session.commit()
    return item_schema.jsonify(item), 200

#DELETE ITEM
@items_bp.route('/<int:item_id>', methods=['DELETE'])
@limiter.limit("5 per day")
def delete_item(item_id):
    item = db.session.get(Item, item_id)
    
    if not item: 
        return jsonify({"error": "Item not found."}), 404
    
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": f"Item {item_id} deleted successfully."}), 200



