from flask import jsonify, request
from marshmallow import ValidationError
from app.blueprints.user import user_bp
from app.models import User, db, select
from app.extensions import limiter, cache
from .schemas import user_schema, users_schema
from app.utils.util import encode_token, token_required


@user_bp.route("/login", methods=['POST'])
def login():
    try:
        credentials = request.json
        email = credentials['email']
        password = credentials['password']
    except KeyError:
        return jsonify({'messages': 'Invalid payload, expecting username and password'}), 400
    
    query = select(User).where(User.email == email)
    user = db.session.execute(query).scalar_one_or_none() 
    
    if user and user.password == password:
        auth_token = encode_token(user.id, user.role.role_name)
        
        response = {
            "status": "success",
            "message": "Successfully Logged In",
            "auth_token": auth_token
        }
        return jsonify(response), 200
    else:
        return jsonify({'message': "Invalid email or password"}), 401

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

#DELETE a User:
@user_bp.route('/users', methods=['DELETE'])
@token_required
def delete_user(user_id): 
    query = select(User).where(User.id == user_id)
    user = db.session.execute(query).scalars().first()
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"successfully deleted user {user_id}"})