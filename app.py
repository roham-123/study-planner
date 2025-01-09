from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

# App configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Local SQLite for now
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize extensions
db = SQLAlchemy(app) 
bcrypt = Bcrypt(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    return "Welcome to the Smart Study Planner!"

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data['email']
    username = data['username']
    password = data['password']

    # Check if email already exists
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'message': 'Email already exists'}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create new user
    new_user = User(email=email, username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    # Check if user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'Invalid email or password'}), 401

    # Check the password
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid email or password'}), 401

    session['user_id'] = user.id
    return jsonify({'message': 'Login successful'}), 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)