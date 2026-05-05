"""
Supabase Database Interface for VaultX
Provides database operations using Supabase
"""

from supabase import create_client, Client
from dotenv import load_dotenv
import os
from typing import Optional, List, Dict, Any
from datetime import datetime

load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_KEY')

# Initialize Supabase client
supabase: Optional[Client] = None

def init_supabase() -> Client:
    """Initialize Supabase client"""
    global supabase
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
    
    if supabase is None:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    return supabase

def get_supabase() -> Client:
    """Get Supabase client instance"""
    if supabase is None:
        return init_supabase()
    return supabase


# ============================================================
# USER OPERATIONS
# ============================================================

def create_user(username: str, email: str, password_hash: str) -> Optional[Dict[str, Any]]:
    """Create a new user"""
    try:
        client = get_supabase()
        response = client.table('users').insert({
            'username': username,
            'email': email,
            'password': password_hash
        }).execute()
        
        if response.data:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Get user by username"""
    try:
        client = get_supabase()
        response = client.table('users').select('*').eq('username', username).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error getting user: {e}")
        return None

def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user by ID"""
    try:
        client = get_supabase()
        response = client.table('users').select('*').eq('id', user_id).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
    except Exception as e:
        print(f"Error getting user by ID: {e}")
        return None

def update_user(user_id: str, **kwargs) -> bool:
    """Update user information"""
    try:
        client = get_supabase()
        response = client.table('users').update(kwargs).eq('id', user_id).execute()
        return bool(response.data)
    except Exception as e:
        print(f"Error updating user: {e}")
        return False


# ============================================================
# FILE HISTORY OPERATIONS
# ============================================================

def log_file_action(username: str, filename: Optional[str], action: str, ip_address: str, user_id: Optional[str] = None) -> bool:
    """Log a file action to history"""
    try:
        client = get_supabase()
        
        data = {
            'username': username,
            'filename': filename,
            'action': action,
            'ip_address': ip_address
        }
        
        if user_id:
            data['user_id'] = user_id
        
        response = client.table('file_history').insert(data).execute()
        return bool(response.data)
    except Exception as e:
        print(f"Error logging file action: {e}")
        return False

def get_user_history(username: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Get user's file history"""
    try:
        client = get_supabase()
        response = client.table('file_history')\
            .select('filename, action, ip_address, created_at')\
            .eq('username', username)\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"Error getting user history: {e}")
        return []

def get_recent_history(username: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Get recent file history for dashboard"""
    try:
        client = get_supabase()
        response = client.table('file_history')\
            .select('filename, action, created_at')\
            .eq('username', username)\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"Error getting recent history: {e}")
        return []


# ============================================================
# CONNECTION LOG OPERATIONS
# ============================================================

def log_connection(ip_address: str, method: str, path: str, status_code: int) -> bool:
    """Log a connection"""
    try:
        client = get_supabase()
        response = client.table('connection_logs').insert({
            'ip_address': ip_address,
            'method': method,
            'path': path,
            'status_code': status_code
        }).execute()
        
        return bool(response.data)
    except Exception as e:
        print(f"Error logging connection: {e}")
        return False

def get_recent_connections(limit: int = 50) -> List[Dict[str, Any]]:
    """Get recent connection logs"""
    try:
        client = get_supabase()
        response = client.table('connection_logs')\
            .select('*')\
            .order('created_at', desc=True)\
            .limit(limit)\
            .execute()
        
        return response.data if response.data else []
    except Exception as e:
        print(f"Error getting connection logs: {e}")
        return []


# ============================================================
# STORAGE OPERATIONS (for encrypted files)
# ============================================================

def upload_encrypted_file(file_path: str, file_name: str, username: str) -> Optional[str]:
    """Upload encrypted file to Supabase Storage"""
    try:
        client = get_supabase()
        
        # Create user-specific path
        storage_path = f"{username}/{file_name}"
        
        with open(file_path, 'rb') as f:
            response = client.storage.from_('encrypted-files').upload(
                storage_path,
                f,
                file_options={"content-type": "application/octet-stream"}
            )
        
        if response:
            return storage_path
        return None
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None

def download_encrypted_file(storage_path: str, local_path: str) -> bool:
    """Download encrypted file from Supabase Storage"""
    try:
        client = get_supabase()
        
        response = client.storage.from_('encrypted-files').download(storage_path)
        
        if response:
            with open(local_path, 'wb') as f:
                f.write(response)
            return True
        return False
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False

def delete_encrypted_file(storage_path: str) -> bool:
    """Delete encrypted file from Supabase Storage"""
    try:
        client = get_supabase()
        response = client.storage.from_('encrypted-files').remove([storage_path])
        return bool(response)
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False

def list_user_files(username: str) -> List[str]:
    """List all files for a user"""
    try:
        client = get_supabase()
        response = client.storage.from_('encrypted-files').list(username)
        
        if response:
            return [file['name'] for file in response]
        return []
    except Exception as e:
        print(f"Error listing files: {e}")
        return []


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def test_connection() -> bool:
    """Test Supabase connection"""
    try:
        client = get_supabase()
        # Try a simple query
        response = client.table('users').select('count').limit(1).execute()
        return True
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False

def get_stats() -> Dict[str, int]:
    """Get database statistics"""
    try:
        client = get_supabase()
        
        # Count users
        users_response = client.table('users').select('count').execute()
        users_count = len(users_response.data) if users_response.data else 0
        
        # Count file actions
        history_response = client.table('file_history').select('count').execute()
        history_count = len(history_response.data) if history_response.data else 0
        
        # Count connections
        logs_response = client.table('connection_logs').select('count').execute()
        logs_count = len(logs_response.data) if logs_response.data else 0
        
        return {
            'users': users_count,
            'file_actions': history_count,
            'connections': logs_count
        }
    except Exception as e:
        print(f"Error getting stats: {e}")
        return {'users': 0, 'file_actions': 0, 'connections': 0}


# ============================================================
# INITIALIZATION
# ============================================================

def initialize():
    """Initialize Supabase connection"""
    try:
        init_supabase()
        print("✅ Supabase initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize Supabase: {e}")
        return False


if __name__ == "__main__":
    # Test the connection
    print("Testing Supabase connection...")
    if test_connection():
        print("✅ Connection successful!")
        stats = get_stats()
        print(f"📊 Stats: {stats}")
    else:
        print("❌ Connection failed!")
