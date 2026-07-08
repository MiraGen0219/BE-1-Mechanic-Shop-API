from .schemas import service_ticket_schema, service_tickets_schema, edit_service_ticket_schema
from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import db, ServiceTicket, Mechanic
from . import service_ticket_bp


# CREATE service ticket:
@service_ticket_bp.route("/", methods=['POST'])
def create_service_ticket(): 
    try: 
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_service_ticket = ServiceTicket(**service_ticket_data)
    
    db.session.add(new_service_ticket)
    db.session.commit()
    
    return jsonify(service_ticket_schema.dump(new_service_ticket)), 201


#GET ALL service tickets:
@service_ticket_bp.route("/", methods=['GET'])
def get_service_tickets(): 
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    
    query = select(ServiceTicket)
    
    pagination = db.paginate(query, page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        "service_tickets": service_tickets_schema.dump(pagination.items),
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages
    }), 200


#ASSIGN / PUT Mechanic by ID to Service Ticket by ID:
@service_ticket_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    
    service_ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not service_ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    
    if not mechanic: 
        return jsonify({"error": "Mechanic not found."}), 404
    
    if mechanic not in service_ticket.mechanics:
        service_ticket.mechanics.append(mechanic)
        db.session.commit()
        
    return jsonify(service_ticket_schema.dump(service_ticket)), 200


#REMOVE / PUT Mechanic by ID from Service Ticket by ID: 
@service_ticket_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    
    service_ticket = db.session.get(ServiceTicket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)
    
    if not service_ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    
    if not mechanic: 
        return jsonify({"error": "Mechanic not found."}), 404
    
    if mechanic in service_ticket.mechanics:
        service_ticket.mechanics.remove(mechanic)
        db.session.commit()
        
    return jsonify(service_ticket_schema.dump(service_ticket)), 200


@service_ticket_bp.route("/<int:ticket_id>", methods=['PUT'])
def edit_service_ticket_id(ticket_id):
    try:
        service_ticket_edits = edit_service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    service_ticket = db.session.get(ServiceTicket, ticket_id)
    
    if not service_ticket:
        return jsonify({"error": "Service ticket not found."}), 400
    
    for mechanic_id in service_ticket_edits.get('add_mechanic_ids', []):
        mechanic = db.session.get(Mechanic, mechanic_id)
        
        if mechanic and mechanic not in service_ticket.mechanics: 
            service_ticket.mechanics.append(mechanic)
            
    for mechanic_id in service_ticket_edits.get('remove_mechanic_ids', []):
        mechanic = db.session.get(Mechanic, mechanic_id)
        
        if mechanic and mechanic in service_ticket.mechanics:
            service_ticket.mechanics.remove(mechanic)
            
    db.session.commit()
    
    return jsonify(service_ticket_schema.dump(service_ticket))