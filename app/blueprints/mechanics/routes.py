from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import db, Mechanic
from . import mechanics_bp
from .schemas import MechanicSchema, mechanic_schema, mechanics_schema

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)


#CREATE / POST a mechanic:
@mechanics_bp.route("/", methods=['POST'])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Mechanic).where(Mechanic.email == mechanic_data['email']) 
    existing_mechanic = db.session.execute(query).scalars().all()
    
    if existing_mechanic:
        return jsonify({"error": "Email already associated with a mechanic."}), 400
    
    new_mechanic = Mechanic(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()
    
    return jsonify(mechanic_schema.dump(new_mechanic)), 201

#GET ALL mechanics:
@mechanics_bp.route("/", methods=['GET'])
def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    
    return jsonify(mechanics_schema.dump(mechanics)), 200

@mechanics_bp.route("/search", methods=['GET'])
def search_book():
    name = request.args.get("name")
    
    query = select(Mechanic).where(Mechanic.name.like(f"%{name}%"))
    mechanics = db.session.execute(query).scalars().all()
    
    return jsonify(mechanics_schema.dump(mechanics)), 200

#UPDATE / EDIT a mechanic: 
@mechanics_bp.route("/<int:mechanic_id>", methods=['PUT'])
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not mechanic: 
        return jsonify({"error": "Mechanic not found"}), 404
    
    try:
        mechanic_data = mechanic_schema.load(request.json, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)
    
    db.session.commit()
    
    return jsonify(mechanic_schema.dump(mechanic)), 200

#DELETE a mechanic:
@mechanics_bp.route("/<int:mechanic_id>", methods=['DELETE'])
def delete_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not mechanic:
        return jsonify({"error": "Mechanic not found"}), 404
    
    db.session.delete(mechanic)
    db.session.commit()
    
    return jsonify({"message": "Mechanic deleted successfully"}), 200

@mechanics_bp.route("/frequent", methods=['GET'])
def frequent_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    
    mechanics_by_ticket_count = []
    
    for mechanic in mechanics:
        mechanics_by_ticket_count.append({
            "id": mechanic.id,
            "name": mechanic.name,
            "email": mechanic.email,
            "ticket_count": len(mechanic.service_tickets)
        })
        
        mechanics_by_ticket_count.sort(
            key=lambda mechanic: mechanic["ticket_count"],
            reverse=True
        )
        
    return jsonify(mechanics_by_ticket_count), 200
