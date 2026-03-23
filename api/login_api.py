from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import re

login_bp = Blueprint('login_bp', __name__, url_prefix='/api/auth')

# Simple in-memory user store (replace with DB model for production)
_users = {}

def valid_email(email):
    return re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email) is not None

class LoginAPI:
    pass

@login_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    name     = (data.get('name') or '').strip()
    email    = (data.get('email') or '').strip().lower()
    password = (data.get('password') or '').strip()

    if len(name) < 2:
        return jsonify({'error': 'Name must be at least 2 characters'}), 400
    if not valid_email(email):
        return jsonify({'error': 'Invalid email address'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    if email in _users:
        return jsonify({'error': 'An account with this email already exists'}), 409

    _users[email] = {
        'name':     name,
        'email':    email,
        'password': generate_password_hash(password),
    }
    session['user'] = {'name': name, 'email': email}
    return jsonify({'message': 'Account created successfully', 'name': name, 'email': email}), 201


@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    email    = (data.get('email') or '').strip().lower()
    password = (data.get('password') or '').strip()

    if not valid_email(email) or len(password) < 6:
        return jsonify({'error': 'Invalid email or password'}), 400

    user = _users.get(email)
    if not user or not check_password_hash(user['password'], password):
        return jsonify({'error': 'Incorrect email or password'}), 401

    session['user'] = {'name': user['name'], 'email': email}
    return jsonify({'message': 'Login successful', 'name': user['name'], 'email': email}), 200


@login_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    return jsonify({'message': 'Logged out successfully'}), 200


@login_bp.route('/status', methods=['GET'])
def status():
    user = session.get('user')
    if user:
        return jsonify({'logged_in': True, 'name': user['name'], 'email': user['email']}), 200
    return jsonify({'logged_in': False}), 200
