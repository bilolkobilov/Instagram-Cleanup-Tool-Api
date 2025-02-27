from app.api import api_bp
from flask import request, jsonify
from app.services.instagram import get_instagram_client
from app.services.deletion import (
    start_posts_deletion, 
    start_reels_deletion, 
    start_messages_deletion, 
    cancel_deletion,
    get_deletion_stats
)
from app.utils.decorators import require_login

@api_bp.route('/delete', methods=['POST'])
@require_login
def delete_content():
    """Start content deletion process"""
    client = get_instagram_client()
    
    data = request.get_json()
    delete_reels = data.get('delete_reels', False)
    delete_messages = data.get('delete_messages', False)
    max_items = data.get('max_items')
    
    if max_items is not None:
        try:
            max_items = int(max_items)
            if max_items <= 0:
                return jsonify({'success': False, 'error': 'Maximum items must be a positive number'}), 400
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid maximum items value'}), 400
    
    if delete_reels:
        start_reels_deletion(client, max_items)
        return jsonify({'success': True, 'message': 'Reels deletion process started'})
    elif delete_messages:
        start_messages_deletion(client, max_items)
        return jsonify({'success': True, 'message': 'Messages deletion process started'})
    else:
        start_posts_deletion(client, max_items)
        return jsonify({'success': True, 'message': 'Posts deletion process started'})

@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get current deletion statistics"""
    stats = get_deletion_stats()
    return jsonify(stats)

@api_bp.route('/cancel', methods=['POST'])
def cancel():
    """Cancel ongoing deletion process"""
    if cancel_deletion():
        return jsonify({'success': True, 'message': 'Deletion canceled'})
    else:
        return jsonify({'success': False, 'message': 'No deletion in progress'})