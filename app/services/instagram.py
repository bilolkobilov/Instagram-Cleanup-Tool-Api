from instagrapi import Client
import threading

_client = None
_client_lock = threading.Lock()

def create_instagram_client(username, password):
    """
    Create and authenticate Instagram client
    """
    global _client
    
    with _client_lock:
        client = Client()
        client.login(username, password)
        _client = client
        return client

def get_instagram_client():
    """
    Get the current Instagram client instance
    """
    return _client

def clear_instagram_client():
    """
    Logout and clear the Instagram client
    """
    global _client
    
    with _client_lock:
        if _client:
            _client.logout()
            _client = None