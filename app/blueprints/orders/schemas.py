from app.extensions import ma
from app.models import Order, OrderItem
from marshmallow import fields
from app.blueprints.items.schemas import ItemSchema

class ReceiptItemSchema(ma.Schema):
    item = fields.String(required=True)
    quantity = fields.Integer(required=True)
    price = fields.Float(required=True)
    subtotal = fields.Float(required=True)
    
class ReceiptSchema(ma.Schema):
    order_id = fields.Integer(required=True)
    customer_id = fields.Integer(required=True)
    order_date = fields.Date(required=True)
    items = fields.List(fields.Nested(ReceiptItemSchema), required=True)
    total = fields.Float(required=True)
    
receipt_schema = ReceiptSchema()
    

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta: 
        model = Order    
        include_relationships = True
    order_items = fields.Nested("OrderItemSchema", exclude=['id'], many=True)
    
class OrderItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OrderItem 
    item = fields.Nested("ItemSchema", exclude=["id"])
        
        
class CreateOrderSchema(ma.Schema):
    '''
    {
        customer_id: 1
        item_quantity: [{item_id: 1, item_quantity: 3}]
        
    }
    '''
    customer_id = fields.Int(required=True)
    item_quantity = fields.Nested("ItemQuantitySchema", many=True)
    
class ItemQuantitySchema(ma.Schema):
    item_id = fields.Int(required=True)
    item_quantity = fields.Int(required=True)
    
        
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
create_order_schema = CreateOrderSchema()
receipt_schema = ReceiptSchema()
