from app.extensions import ma
from marshmallow import fields

class UserSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    
    
user_schema = UserSchema()
users_schema = UserSchema(many=True)