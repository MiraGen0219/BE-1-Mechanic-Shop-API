from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Inventory
from app import ma

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta: 
        model = Inventory
        include_fk = True
        
inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)