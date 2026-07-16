from flask import jsonify, request
from marshmallow import ValidationError
from app.blueprints.users import user_bp
from app.models import User, db
from sqlalchemy import select
from app.extensions import limiter, cache
from .schemas import user_schema, users_schema
from app.utils.util import encode_token, token_required


@user_bp.route("/login", methods=['POST'])
def login():
    try:
        credentials = request.json
        email = credentials['email']
        password = credentials['password']
    except (KeyError, TypeError):
        return jsonify({'message': 'Invalid payload, expecting email and password'}), 400
    
    query = select(User).where(User.email == email)
    user = db.session.execute(query).scalar_one_or_none() 
    
    if user and user.password == password:
        auth_token = encode_token(user.id)
        
        return jsonify ({
            "status": "success",
            "message": "Successfully Logged In",
            "auth_token": auth_token
        }), 200
    
    return jsonify({'message': "Invalid email or password"}), 401

#CREATE / POST a User:
@user_bp.route("/", methods=["POST"])
@limiter.limit("3 per hour")
def create_user():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    existing_email = db.session.execute(
        select(User).where(
            User.email == user_data["email"]
        )
    ).scalar_one_or_none()

    if existing_email:
        return jsonify({
            "message": "A user with that email already exists"
        }), 409

    existing_username = db.session.execute(
        select(User).where(
            User.username == user_data["username"]
        )
    ).scalar_one_or_none()

    if existing_username:
        return jsonify({
            "message": "A user with that username already exists"
        }), 409

    new_user = User(
        username=user_data["username"],
        email=user_data["email"],
        password=user_data["password"]
    )

    db.session.add(new_user)
    db.session.commit()
    cache.clear()

    return user_schema.jsonify(new_user), 201

#GET / RETRIEVE Users:
@user_bp.route('/', methods=['GET'])
@cache.cached(timeout=60)
def get_users():
    query = select(User)
    result = db.session.execute(query).scalars().all()
    return users_schema.jsonify(result), 200 

#DELETE a User:
@user_bp.route('/', methods=['DELETE'])
@token_required
def delete_user(user_id): 
    user = db.session.get(User, user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    cache.clear()
    
    return jsonify({"message": f"Successfully deleted user {user_id}"}), 200