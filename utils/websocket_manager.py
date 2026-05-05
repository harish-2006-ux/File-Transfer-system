"""
WebSocket Manager for Real-time Updates
Live activity feed, file uploads, instant notifications
"""

from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime
from typing import Dict, Any, List
import json


class WebSocketManager:
    """Manage WebSocket connections and real-time updates"""
    
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
        self.active_users = {}  # {user_id: [session_ids]}
        self.user_rooms = {}  # {session_id: user_id}
        
        # Register event handlers
        self.register_handlers()
    
    def register_handlers(self):
        """Register WebSocket event handlers"""
        
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection"""
            print(f"Client connected: {request.sid}")
            emit('connection_response', {
                'status': 'connected',
                'timestamp': datetime.now().isoformat()
            })
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection"""
            session_id = request.sid
            if session_id in self.user_rooms:
                user_id = self.user_rooms[session_id]
                self.remove_user_session(user_id, session_id)
            print(f"Client disconnected: {session_id}")
        
        @self.socketio.on('join')
        def handle_join(data):
            """Handle user joining their personal room"""
            user_id = data.get('user_id')
            username = data.get('username')
            
            if user_id:
                room = f"user_{user_id}"
                join_room(room)
                
                # Track user session
                self.add_user_session(user_id, request.sid)
                
                emit('joined', {
                    'room': room,
                    'username': username,
                    'timestamp': datetime.now().isoformat()
                })
                
                print(f"User {username} joined room {room}")
        
        @self.socketio.on('leave')
        def handle_leave(data):
            """Handle user leaving their room"""
            user_id = data.get('user_id')
            
            if user_id:
                room = f"user_{user_id}"
                leave_room(room)
                
                # Remove user session
                self.remove_user_session(user_id, request.sid)
                
                emit('left', {
                    'room': room,
                    'timestamp': datetime.now().isoformat()
                })
        
        @self.socketio.on('request_stats')
        def handle_stats_request():
            """Handle request for system stats"""
            # This will be called from the main app
            pass
    
    def add_user_session(self, user_id: str, session_id: str):
        """Add user session"""
        if user_id not in self.active_users:
            self.active_users[user_id] = []
        self.active_users[user_id].append(session_id)
        self.user_rooms[session_id] = user_id
    
    def remove_user_session(self, user_id: str, session_id: str):
        """Remove user session"""
        if user_id in self.active_users:
            if session_id in self.active_users[user_id]:
                self.active_users[user_id].remove(session_id)
            if not self.active_users[user_id]:
                del self.active_users[user_id]
        
        if session_id in self.user_rooms:
            del self.user_rooms[session_id]
    
    def is_user_online(self, user_id: str) -> bool:
        """Check if user is online"""
        return user_id in self.active_users and len(self.active_users[user_id]) > 0
    
    def get_online_users_count(self) -> int:
        """Get count of online users"""
        return len(self.active_users)
    
    # Real-time notification methods
    
    def notify_file_upload(self, user_id: str, filename: str, filesize: str):
        """Notify user of file upload"""
        self.socketio.emit('file_uploaded', {
            'filename': filename,
            'filesize': filesize,
            'timestamp': datetime.now().isoformat(),
            'message': f'File "{filename}" uploaded successfully'
        }, room=f"user_{user_id}")
    
    def notify_file_download(self, user_id: str, filename: str):
        """Notify user of file download"""
        self.socketio.emit('file_downloaded', {
            'filename': filename,
            'timestamp': datetime.now().isoformat(),
            'message': f'File "{filename}" downloaded'
        }, room=f"user_{user_id}")
    
    def notify_file_delete(self, user_id: str, filename: str):
        """Notify user of file deletion"""
        self.socketio.emit('file_deleted', {
            'filename': filename,
            'timestamp': datetime.now().isoformat(),
            'message': f'File "{filename}" deleted'
        }, room=f"user_{user_id}")
    
    def notify_login(self, user_id: str, ip: str, location: Dict[str, Any]):
        """Notify user of new login"""
        self.socketio.emit('new_login', {
            'ip': ip,
            'location': location,
            'timestamp': datetime.now().isoformat(),
            'message': 'New login detected'
        }, room=f"user_{user_id}")
    
    def notify_suspicious_activity(self, user_id: str, details: Dict[str, Any]):
        """Notify user of suspicious activity"""
        self.socketio.emit('suspicious_activity', {
            'details': details,
            'timestamp': datetime.now().isoformat(),
            'message': '⚠️ Suspicious activity detected',
            'severity': 'high'
        }, room=f"user_{user_id}")
    
    def broadcast_system_stats(self, stats: Dict[str, Any]):
        """Broadcast system stats to all connected clients"""
        self.socketio.emit('system_stats', {
            'stats': stats,
            'timestamp': datetime.now().isoformat()
        }, broadcast=True)
    
    def send_activity_update(self, user_id: str, activity: Dict[str, Any]):
        """Send activity update to user"""
        self.socketio.emit('activity_update', {
            'activity': activity,
            'timestamp': datetime.now().isoformat()
        }, room=f"user_{user_id}")
    
    def send_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        notification_type: str = 'info',
        data: Optional[Dict[str, Any]] = None
    ):
        """Send generic notification to user"""
        self.socketio.emit('notification', {
            'title': title,
            'message': message,
            'type': notification_type,  # info, success, warning, error
            'data': data or {},
            'timestamp': datetime.now().isoformat()
        }, room=f"user_{user_id}")
    
    def broadcast_announcement(self, title: str, message: str):
        """Broadcast announcement to all users"""
        self.socketio.emit('announcement', {
            'title': title,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }, broadcast=True)


# Initialize WebSocket manager (will be set from main app)
ws_manager: Optional[WebSocketManager] = None


def init_websocket_manager(socketio: SocketIO) -> WebSocketManager:
    """Initialize WebSocket manager"""
    global ws_manager
    ws_manager = WebSocketManager(socketio)
    return ws_manager


def get_websocket_manager() -> Optional[WebSocketManager]:
    """Get WebSocket manager instance"""
    return ws_manager


if __name__ == "__main__":
    print("WebSocket Manager module")
    print("This module should be imported and initialized with Flask-SocketIO")
