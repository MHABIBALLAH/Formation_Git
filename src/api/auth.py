from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from src.api.app import db, bcrypt
from src.core.auth.models import User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    """Registers a new user."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409 # Conflict
    
    print("user=",username , "password=",password)
    
    #hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    hashed_password = password
    new_user = User(username=username, password_hash=hashed_password, role='user')
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth.route('/login', methods=['POST'])
def login():
    """Logs in a user."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    

    #username = 'Anass1'
    #password = '123'
    print("user=",username , "password=",password)

    #if user and bcrypt.check_password_hash(user.password_hash, password):
    if user and password:        
        print("user et password OK  ")
        login_user(user, remember=True) # `remember=True` adds a "remember me" cookie
        return jsonify({'message': 'Login successful', 'user': {'username': user.username, 'role': user.role}}), 200
    print("user et password KO  ")
    return jsonify({'error': 'Invalid credentials'}), 401

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logs out the current user."""
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@auth.route('/profile')
@login_required
def get_current_user_profile():
    """Returns the profile of the currently logged-in user."""
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'role': current_user.role
    })
