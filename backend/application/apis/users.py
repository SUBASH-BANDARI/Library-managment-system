from application.models import *
from flask import jsonify, request
from application.database import db
from main import app
from flask_bcrypt import Bcrypt
from application.auth import admin_required
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        user = Users.query.filter_by(email=data['email']).first()
        if user:
            return jsonify({'message': 'User already exists'}), 409
        else:
            b=Bcrypt()
            hashed_password = b.generate_password_hash(data['password'])
            new_user = Users(email=data['email'], username=data['username'] ,password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            access_token = create_access_token(
                identity={"email": data['email']}, additional_claims={"is_administrator": False}
            )
            return jsonify({"token": access_token, "user": new_user.username}), 201
            
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = Users.query.filter_by(email=data['email']).first()
        if user:
            b=Bcrypt()
            if b.check_password_hash(user.password, data['password']):
                #check if admin and pass admin to frontend
                access_token = create_access_token(
                identity={"email":user.email}, additional_claims={"is_administrator": user.is_admin}
                    )
                print(user.is_admin)
                return jsonify({"token": access_token, "user": user.username, "is_admin": user.is_admin }), 200
            else:
                return jsonify({'message': 'Invalid password'}), 401
        else:
            return jsonify({'message': 'User does not exist'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    try:
        users = Users.query.all()
        return jsonify([user.serialize() for user in users]), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500

@app.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    try:
        user = Users.query.get(id)
        if user:
            user_data = {}
            user_data['id'] = user.id
            user_data['email'] = user.email
            user_data['username'] = user.username
            user_data['admin'] = user.is_admin
            return jsonify({ 'user' : user_data }), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500
    
@app.route('/current_user', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user = Users.query.filter_by(email=get_jwt_identity()['email']).first()
        return jsonify({'user': user.serialize()}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': 'Something went wrong'}), 500