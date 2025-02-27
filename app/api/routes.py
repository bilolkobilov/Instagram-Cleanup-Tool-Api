from app.api import api_bp
from flask import jsonify
from app.services.instagram import get_instagram_client

@api_bp.route('/status', methods=['GET'])
def status():
    """Check if user is logged in"""
    client = get_instagram_client()
    return jsonify({'loggedIn': client is not None})