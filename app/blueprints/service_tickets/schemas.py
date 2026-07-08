from app.models import ServiceTicket
from app.extensions import ma
from marshmallow import fields

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        load_instance = False
        include_relationships = True
        
class EditServiceTicketSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required=False)
    remove_mechanic_ids = fields.List(fields.Int(), required=False)
    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")
        
service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
edit_service_ticket_schema = EditServiceTicketSchema()