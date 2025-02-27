import threading
import time

_is_deleting = False
_deleted_count = 0
_total_items = 0
_deletion_start_time = None
_max_items_to_delete = None
_deletion_lock = threading.Lock()

def start_posts_deletion(client, max_items=None):
    """
    Start a thread to delete posts
    """
    global _is_deleting, _deleted_count, _total_items, _deletion_start_time, _max_items_to_delete
    
    with _deletion_lock:
        if _is_deleting:
            return False
            
        _is_deleting = True
        _deleted_count = 0
        _deletion_start_time = time.time()
        _max_items_to_delete = max_items
        
        thread = threading.Thread(target=_delete_posts_thread, args=(client,), daemon=True)
        thread.start()
        return True

def start_reels_deletion(client, max_items=None):
    """
    Start a thread to delete reels
    """
    global _is_deleting, _deleted_count, _total_items, _deletion_start_time, _max_items_to_delete
    
    with _deletion_lock:
        if _is_deleting:
            return False
            
        _is_deleting = True
        _deleted_count = 0
        _deletion_start_time = time.time()
        _max_items_to_delete = max_items
        
        thread = threading.Thread(target=_delete_reels_thread, args=(client,), daemon=True)
        thread.start()
        return True

def start_messages_deletion(client, max_items=None):
    """
    Start a thread to delete message threads
    """
    global _is_deleting, _deleted_count, _total_items, _deletion_start_time, _max_items_to_delete
    
    with _deletion_lock:
        if _is_deleting:
            return False
            
        _is_deleting = True
        _deleted_count = 0
        _deletion_start_time = time.time()
        _max_items_to_delete = max_items
        
        thread = threading.Thread(target=_delete_messages_thread, args=(client,), daemon=True)
        thread.start()
        return True

def cancel_deletion():
    """
    Cancel the ongoing deletion process
    """
    global _is_deleting
    
    with _deletion_lock:
        if not _is_deleting:
            return False
            
        _is_deleting = False
        return True

def get_deletion_stats():
    """
    Get current deletion statistics
    """
    elapsed_time = 0
    if _deletion_start_time:
        elapsed_time = int(time.time() - _deletion_start_time)
    
    return {
        'deleted': _deleted_count,
        'total': _total_items,
        'in_progress': _is_deleting,
        'elapsed_seconds': elapsed_time
    }

def _delete_posts_thread(client):
    """Deletes all posts with improved error handling and rate limiting"""
    global _is_deleting, _deleted_count, _total_items
    try:
        user_id = client.user_id
        medias = client.user_medias(user_id, 100)
        
        if _max_items_to_delete is not None and len(medias) > _max_items_to_delete:
            medias = medias[:_max_items_to_delete]
        
        with _deletion_lock:
            _total_items = len(medias)
        
        if _total_items == 0:
            with _deletion_lock:
                _is_deleting = False
            return
        
        for i, media in enumerate(medias):
            if not _is_deleting:
                break
                
            try:
                if i > 0:
                    delay = 1.5 + (1.5 * (i % 2))
                    time.sleep(delay)
                    
                client.media_delete(media.id)
                
                with _deletion_lock:
                    _deleted_count += 1
                
                if _deleted_count % 10 == 0 and _deleted_count < _total_items:
                    time.sleep(5)
                    
            except Exception:
                time.sleep(5)
                
    except Exception:
        pass
    finally:
        with _deletion_lock:
            _is_deleting = False

def _delete_reels_thread(client):
    """Deletes all reels with improved error handling and rate limiting"""
    global _is_deleting, _deleted_count, _total_items
    try:
        user_id = client.user_id
        reels = client.user_clips(user_id, 100)
        
        if _max_items_to_delete is not None and len(reels) > _max_items_to_delete:
            reels = reels[:_max_items_to_delete]
        
        with _deletion_lock:
            _total_items = len(reels)
        
        if _total_items == 0:
            with _deletion_lock:
                _is_deleting = False
            return
        
        for i, reel in enumerate(reels):
            if not _is_deleting:
                break
                
            try:
                if i > 0:
                    delay = 1.5 + (1.5 * (i % 2))
                    time.sleep(delay)
                    
                client.media_delete(reel.id)
                
                with _deletion_lock:
                    _deleted_count += 1
                
                if _deleted_count % 10 == 0 and _deleted_count < _total_items:
                    time.sleep(5)
                    
            except Exception:
                time.sleep(5)
                
    except Exception:
        pass
    finally:
        with _deletion_lock:
            _is_deleting = False

def _delete_messages_thread(client):
    """Deletes all message threads from inbox with rate limiting"""
    global _is_deleting, _deleted_count, _total_items
    try:
        threads = client.direct_threads(amount=100)
        
        if _max_items_to_delete is not None and len(threads) > _max_items_to_delete:
            threads = threads[:_max_items_to_delete]
        
        with _deletion_lock:
            _total_items = len(threads)
        
        if _total_items == 0:
            with _deletion_lock:
                _is_deleting = False
            return
        
        for i, thread in enumerate(threads):
            if not _is_deleting:
                break
                
            try:
                if i > 0:
                    delay = 1.5 + (1.5 * (i % 2))
                    time.sleep(delay)
                    
                client.direct_thread_hide(thread.id)
                
                with _deletion_lock:
                    _deleted_count += 1
                
                if _deleted_count % 10 == 0 and _deleted_count < _total_items:
                    time.sleep(5)
                    
            except Exception:
                time.sleep(5)
                
    except Exception:
        pass
    finally:
        with _deletion_lock:
            _is_deleting = False