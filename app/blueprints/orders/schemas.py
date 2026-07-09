from app.extensions import ma
from app.models import Order, OrderItem
from marshmallow import fields
from app.blueprints.items.schemas import ItemSchema

class ReceiptSchema(ma.Schema):
    '''
    total: 39.02
    order: {
        order_id: 1,
        customer_id: 1,
        order_date: 2024-10-08,
        order_items: [
            {
                item: {item_name: "Brake Pads", price: 68.99},
                quantity: 2
            }
            ]
            }
    '''
    total = fields.Int(required=True)
    order = fields.Nested("OrderSchema")
    

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
