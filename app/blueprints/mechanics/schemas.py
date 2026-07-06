from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import Mechanic
from app.extensions import ma



class MechanicSchema(SQLAlchemyAutoSchema):
    class Meta:
        model= Mechanic


mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)