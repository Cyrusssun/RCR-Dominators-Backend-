from flask import Blueprint, request, jsonify, session
import re
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.railroad_user import RailroadUser

# 创建 Blueprint - 这是关键！
login_bp = Blueprint('login_bp', __name__, url_prefix='/api/auth')

def valid_email(email):
    return re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email) is not None

@login_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    name = (data.get('name') or '').strip()
    email = (data.get('email') or '').strip().lower()
    password = (data.get('password') or '').strip()

    if len(name) < 2:
        return jsonify({'error': 'Name must be at least 2 characters'}), 400
    if not valid_email(email):
        return jsonify({'error': 'Invalid email address'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    if RailroadUser.query.filter_by(email=email).first():
        return jsonify({'error': 'An account with this email already exists'}), 409

    user = RailroadUser(name=name, email=email, password=password)
    result = user.create()
    if not result:
        return jsonify({'error': 'Registration failed. Please try again.'}), 500

    session['user'] = {'name': name, 'email': email}
    return jsonify({'message': 'Account created successfully', 'name': name, 'email': email}), 201

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    email = (data.get('email') or '').strip().lower()
    password = (data.get('password') or '').strip()

    if not valid_email(email) or len(password) < 6:
        return jsonify({'error': 'Invalid email or password'}), 400

    user = RailroadUser.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Incorrect email or password'}), 401

    session['user'] = {'name': user.name, 'email': email}
    print(f"Login successful: {email}, Session: {session}")  # 调试信息
    return jsonify({'message': 'Login successful', 'name': user.name, 'email': email}), 200

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

@login_bp.route('/change-password', methods=['POST'])
def change_password():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    current = (data.get('current_password') or '').strip()
    new_pw = (data.get('new_password') or '').strip()

    if len(current) < 6 or len(new_pw) < 6:
        return jsonify({'error': 'Passwords must be at least 6 characters'}), 400

    logged_in = session.get('user')
    if not logged_in:
        return jsonify({'error': 'Not logged in'}), 401

    user = RailroadUser.query.filter_by(email=logged_in['email']).first()
    if not user or not user.check_password(current):
        return jsonify({'error': 'Current password is incorrect'}), 401

    user.update_password(new_pw)
    return jsonify({'message': 'Password updated successfully'}), 200