from functools import wraps
from flask import jsonify
from app.services.instagram import get_instagram_client

def require_login(f):
    """
    Decorator to require Instagram login
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client = get_instagram_client()
        if not client:
            return jsonify({'success': False, 'error': 'Not logged in'}), 401
        return f(*args, **kwargs)
    return decorated_function