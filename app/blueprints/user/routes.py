from flask import jsonify, request
from marshmallow import ValidationError
from app.blueprints.user import user_bp
from app.models import User, db, select
from app.extensions import limiter, cache
from .schemas import user_schema, users_schema


#CREATE / POST a User:
@user_bp.route("/users", methods=['POST'])
@limiter.limit("3 per hour") #a client can only attempt to make 3 users per hour
def create_user():
    try: 
        # Deserialize and validate input data
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    #use data to create an instance of User
    new_user = User(name=user_data['name'], email=user_data['email'], password=user_data['password'])
    
    #save new_user to the database
    db.session.add(new_user)
    db.session.commit()
    
    #use schema to return the serialized data of the created user
    return user_schema.jsonify(new_user), 201

#GET / RETRIEVE Users:
@user_bp.route('/users', methods=['GET'])
@cache.cached(timeout=60)
def get_users():
    query = select(User)
    result = db.session.execute(query).scalars().all()
    return users_schema.jsonify(result), 200 