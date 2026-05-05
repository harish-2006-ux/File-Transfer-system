"""
Analytics and Statistics Module
Usage statistics, charts data, and insights
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from collections import defaultdict
from database.supabase_client import get_supabase
import json


class AnalyticsService:
    """Handle analytics and statistics"""
    
    def __init__(self):
        try:
            self.client = get_supabase()
        except (ValueError, Exception) as e:
            print(f"⚠️  Analytics using SQLite fallback: {e}")
            self.client = None
    
    def get_user_statistics(self, username: str, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive user statistics"""
        if not self.client:
            # Fallback to SQLite
            return self._get_user_statistics_sqlite(username, days)
        
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        try:
            # Get file history
            history_response = self.client.table('file_history')\
                .select('*')\
                .eq('username', username)\
                .gte('created_at', cutoff_date)\
                .execute()
            
            history = history_response.data if history_response.data else []
            
            # Calculate statistics
            stats = {
                'total_actions': len(history),
                'uploads': sum(1 for h in history if h['action'] == 'UPLOAD'),
                'downloads': sum(1 for h in history if h['action'] == 'DOWNLOAD'),
                'deletes': sum(1 for h in history if h['action'] == 'DELETE'),
                'logins': sum(1 for h in history if h['action'] == 'LOGIN'),
                'period_days': days
            }
            
            # Activity by day
            activity_by_day = defaultdict(int)
            for h in history:
                date = h['created_at'][:10]  # Get date part
                activity_by_day[date] += 1
            
            stats['activity_by_day'] = dict(activity_by_day)
            
            # Activity by type
            activity_by_type = defaultdict(int)
            for h in history:
                activity_by_type[h['action']] += 1
            
            stats['activity_by_type'] = dict(activity_by_type)
            
            # Most active hours
            activity_by_hour = defaultdict(int)
            for h in history:
                hour = int(h['created_at'][11:13])  # Get hour
                activity_by_hour[hour] += 1
            
            stats['activity_by_hour'] = dict(activity_by_hour)
            
            # Recent files
            recent_files = [
                {
                    'filename': h['filename'],
                    'action': h['action'],
                    'timestamp': h['created_at']
                }
                for h in sorted(history, key=lambda x: x['created_at'], reverse=True)[:10]
                if h['filename']
            ]
            
            stats['recent_files'] = recent_files
            
            return stats
            
        except Exception as e:
            print(f"Error getting user statistics: {e}")
            return self._get_user_statistics_sqlite(username, days)
    
    def _get_user_statistics_sqlite(self, username: str, days: int = 30) -> Dict[str, Any]:
        """Get user statistics from SQLite (fallback)"""
        import sqlite3
        from datetime import datetime, timedelta
        
        try:
            conn = sqlite3.connect("transfers.db")
            cur = conn.cursor()
            
            cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            
            cur.execute(
                "SELECT filename, action, timestamp FROM history WHERE username = ? AND timestamp >= ? ORDER BY id DESC",
                (username, cutoff_date)
            )
            history = cur.fetchall()
            conn.close()
            
            stats = {
                'total_actions': len(history),
                'uploads': sum(1 for h in history if h[1] == 'UPLOAD'),
                'downloads': sum(1 for h in history if h[1] == 'DOWNLOAD'),
                'deletes': sum(1 for h in history if h[1] == 'DELETE'),
                'logins': sum(1 for h in history if h[1] == 'LOGIN'),
                'period_days': days,
                'activity_by_day': {},
                'activity_by_type': {},
                'activity_by_hour': {},
                'recent_files': []
            }
            
            # Activity by type
            activity_by_type = defaultdict(int)
            for h in history:
                activity_by_type[h[1]] += 1
            stats['activity_by_type'] = dict(activity_by_type)
            
            return stats
            
        except Exception as e:
            print(f"Error getting SQLite statistics: {e}")
            return {
                'total_actions': 0,
                'uploads': 0,
                'downloads': 0,
                'deletes': 0,
                'logins': 0,
                'period_days': days,
                'activity_by_day': {},
                'activity_by_type': {},
                'activity_by_hour': {},
                'recent_files': []
            }
    
    def get_system_statistics(self, days: int = 7) -> Dict[str, Any]:
        """Get system-wide statistics"""
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        try:
            # Total users
            users_response = self.client.table('users').select('count').execute()
            total_users = len(users_response.data) if users_response.data else 0
            
            # Total file actions
            history_response = self.client.table('file_history')\
                .select('*')\
                .gte('created_at', cutoff_date)\
                .execute()
            
            history = history_response.data if history_response.data else []
            
            # Connection logs
            logs_response = self.client.table('connection_logs')\
                .select('*')\
                .gte('created_at', cutoff_date)\
                .execute()
            
            logs = logs_response.data if logs_response.data else []
            
            stats = {
                'total_users': total_users,
                'total_actions': len(history),
                'total_requests': len(logs),
                'period_days': days,
                'uploads': sum(1 for h in history if h['action'] == 'UPLOAD'),
                'downloads': sum(1 for h in history if h['action'] == 'DOWNLOAD'),
                'deletes': sum(1 for h in history if h['action'] == 'DELETE'),
                'logins': sum(1 for h in history if h['action'] == 'LOGIN')
            }
            
            # Most active users
            user_activity = defaultdict(int)
            for h in history:
                user_activity[h['username']] += 1
            
            most_active = sorted(
                user_activity.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
            
            stats['most_active_users'] = [
                {'username': username, 'actions': count}
                for username, count in most_active
            ]
            
            # Activity trend
            activity_by_day = defaultdict(int)
            for h in history:
                date = h['created_at'][:10]
                activity_by_day[date] += 1
            
            stats['activity_trend'] = dict(activity_by_day)
            
            # Request status codes
            status_codes = defaultdict(int)
            for log in logs:
                status_codes[log['status_code']] += 1
            
            stats['status_codes'] = dict(status_codes)
            
            return stats
            
        except Exception as e:
            print(f"Error getting system statistics: {e}")
            return {
                'total_users': 0,
                'total_actions': 0,
                'total_requests': 0,
                'period_days': days,
                'uploads': 0,
                'downloads': 0,
                'deletes': 0,
                'logins': 0,
                'most_active_users': [],
                'activity_trend': {},
                'status_codes': {}
            }
    
    def get_chart_data(self, username: str, chart_type: str, days: int = 30) -> Dict[str, Any]:
        """Get data formatted for charts"""
        stats = self.get_user_statistics(username, days)
        
        if chart_type == 'activity_timeline':
            # Format for line chart
            dates = sorted(stats['activity_by_day'].keys())
            return {
                'labels': dates,
                'datasets': [{
                    'label': 'Activity',
                    'data': [stats['activity_by_day'][date] for date in dates]
                }]
            }
        
        elif chart_type == 'activity_distribution':
            # Format for pie chart
            activity_types = stats['activity_by_type']
            return {
                'labels': list(activity_types.keys()),
                'datasets': [{
                    'data': list(activity_types.values())
                }]
            }
        
        elif chart_type == 'hourly_activity':
            # Format for bar chart
            hours = range(24)
            activity_by_hour = stats['activity_by_hour']
            return {
                'labels': [f"{h:02d}:00" for h in hours],
                'datasets': [{
                    'label': 'Actions',
                    'data': [activity_by_hour.get(h, 0) for h in hours]
                }]
            }
        
        return {}
    
    def get_security_insights(self, username: str, days: int = 30) -> Dict[str, Any]:
        """Get security-related insights"""
        if not self.client:
            # Return empty insights for SQLite
            return {
                'total_security_events': 0,
                'total_logins': 0,
                'suspicious_events': 0,
                'failed_logins': 0,
                'unique_ips': 0,
                'period_days': days,
                'recent_events': [],
                'login_locations': {}
            }
        
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        try:
            # Get security events
            events_response = self.client.table('security_events')\
                .select('*')\
                .eq('username', username)\
                .gte('created_at', cutoff_date)\
                .execute()
            
            events = events_response.data if events_response.data else []
            
            # Get login history
            history_response = self.client.table('file_history')\
                .select('*')\
                .eq('username', username)\
                .eq('action', 'LOGIN')\
                .gte('created_at', cutoff_date)\
                .execute()
            
            logins = history_response.data if history_response.data else []
            
            insights = {
                'total_security_events': len(events),
                'total_logins': len(logins),
                'suspicious_events': sum(1 for e in events if e['event_type'] == 'SUSPICIOUS_LOGIN'),
                'failed_logins': sum(1 for e in events if e['event_type'] == 'FAILED_LOGIN'),
                'unique_ips': len(set(e['ip_address'] for e in events)),
                'period_days': days
            }
            
            # Recent security events
            insights['recent_events'] = [
                {
                    'type': e['event_type'],
                    'ip': e['ip_address'],
                    'timestamp': e['created_at'],
                    'details': json.loads(e['details']) if e.get('details') else {}
                }
                for e in sorted(events, key=lambda x: x['created_at'], reverse=True)[:10]
            ]
            
            # Login locations
            login_locations = defaultdict(int)
            for login in logins:
                ip = login.get('ip_address', 'Unknown')
                login_locations[ip] += 1
            
            insights['login_locations'] = dict(login_locations)
            
            return insights
            
        except Exception as e:
            print(f"Error getting security insights: {e}")
            return {
                'total_security_events': 0,
                'total_logins': 0,
                'suspicious_events': 0,
                'failed_logins': 0,
                'unique_ips': 0,
                'period_days': days,
                'recent_events': [],
                'login_locations': {}
            }
    
    def generate_report(self, username: str, report_type: str = 'summary') -> Dict[str, Any]:
        """Generate comprehensive report"""
        if report_type == 'summary':
            return {
                'user_stats': self.get_user_statistics(username, 30),
                'security_insights': self.get_security_insights(username, 30),
                'generated_at': datetime.now().isoformat()
            }
        
        elif report_type == 'detailed':
            return {
                'user_stats_7d': self.get_user_statistics(username, 7),
                'user_stats_30d': self.get_user_statistics(username, 30),
                'user_stats_90d': self.get_user_statistics(username, 90),
                'security_insights': self.get_security_insights(username, 90),
                'generated_at': datetime.now().isoformat()
            }
        
        return {}


# Global analytics service instance
analytics_service = AnalyticsService()


if __name__ == "__main__":
    print("Analytics Service module")
    print("Use analytics_service to get statistics and insights")
