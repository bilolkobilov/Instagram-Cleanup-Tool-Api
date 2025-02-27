from app.api import api_bp
from flask import request, jsonify
from app.services.instagram import create_instagram_client, get_instagram_client, clear_instagram_client
from app.utils.decorators import require_login

@api_bp.route('/login', methods=['POST'])
def login():
    """Handle Instagram login"""
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'success': False, 'error': 'Invalid or missing credentials'}), 400

    username = data['username']
    password = data['password']

    try:
        client = create_instagram_client(username, password)
        return jsonify({'success': True})
    except Exception as e:
        error_message = str(e)
        if 'challenge_required' in error_message.lower():
            return jsonify({'success': False, 'error': 'Instagram requires verification. Please log in through the app first and try again.'}), 401
        elif 'bad_password' in error_message.lower():
            return jsonify({'success': False, 'error': 'Incorrect password. Please check your credentials.'}), 401
        elif 'invalid_user' in error_message.lower():
            return jsonify({'success': False, 'error': 'Username not found. Please check your credentials.'}), 401
        else:
            return jsonify({'success': False, 'error': f'Login failed: {error_message}'}), 401

@api_bp.route('/logout', methods=['POST'])
@require_login
def logout():
    """Handle Instagram logout"""
    try:
        clear_instagram_client()
        return jsonify({'success': True, 'message': 'Successfully logged out'})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Logout failed: {str(e)}'}), 500