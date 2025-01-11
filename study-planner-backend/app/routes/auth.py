from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    from app import bcrypt, db
    from app.DBmodels import User

    data = request.json
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 400

    # Create a new user
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201


@auth.route('/login', methods=['POST'])
def login():
    from app import bcrypt, db
    from app.DBmodels import User

    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'message': 'Login successful', 'access_token': access_token}), 200