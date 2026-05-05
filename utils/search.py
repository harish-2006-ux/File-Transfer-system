"""
Advanced Search System
Search through files, logs, and activities
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from database.supabase_client import get_supabase
import re


class SearchService:
    """Handle advanced search operations"""
    
    def __init__(self):
        try:
            self.client = get_supabase()
        except (ValueError, Exception) as e:
            print(f"⚠️  Search using SQLite fallback: {e}")
            self.client = None
    
    def search_files(
        self,
        username: str,
        query: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search through user's files
        
        Args:
            username: Username to search for
            query: Search query
            filters: Optional filters (date_from, date_to, action_type)
        
        Returns:
            List of matching file records
        """
        if not self.client:
            # Fallback to SQLite
            return self._search_files_sqlite(username, query, filters)
        
        try:
            # Build query
            db_query = self.client.table('file_history')\
                .select('*')\
                .eq('username', username)
            
            # Apply filters
            if filters:
                if filters.get('date_from'):
                    db_query = db_query.gte('created_at', filters['date_from'])
                
                if filters.get('date_to'):
                    db_query = db_query.lte('created_at', filters['date_to'])
                
                if filters.get('action_type'):
                    db_query = db_query.eq('action', filters['action_type'])
            
            response = db_query.execute()
            results = response.data if response.data else []
            
            # Filter by query (case-insensitive)
            if query:
                query_lower = query.lower()
                results = [
                    r for r in results
                    if r.get('filename') and query_lower in r['filename'].lower()
                ]
            
            # Sort by relevance and date
            results.sort(key=lambda x: x['created_at'], reverse=True)
            
            return results
            
        except Exception as e:
            print(f"Error searching files: {e}")
            return []
    
    def search_activity(
        self,
        username: str,
        query: str,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search through user's activity history
        
        Args:
            username: Username to search for
            query: Search query
            filters: Optional filters
        
        Returns:
            List of matching activity records
        """
        try:
            db_query = self.client.table('file_history')\
                .select('*')\
                .eq('username', username)
            
            # Apply date filters
            if filters:
                if filters.get('date_from'):
                    db_query = db_query.gte('created_at', filters['date_from'])
                
                if filters.get('date_to'):
                    db_query = db_query.lte('created_at', filters['date_to'])
            
            response = db_query.execute()
            results = response.data if response.data else []
            
            # Filter by query
            if query:
                query_lower = query.lower()
                results = [
                    r for r in results
                    if (r.get('filename') and query_lower in r['filename'].lower()) or
                       (r.get('action') and query_lower in r['action'].lower()) or
                       (r.get('ip_address') and query_lower in r['ip_address'].lower())
                ]
            
            results.sort(key=lambda x: x['created_at'], reverse=True)
            
            return results
            
        except Exception as e:
            print(f"Error searching activity: {e}")
            return []
    
    def search_security_events(
        self,
        username: str,
        query: str,
        event_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Search through security events"""
        try:
            db_query = self.client.table('security_events')\
                .select('*')\
                .eq('username', username)
            
            if event_type:
                db_query = db_query.eq('event_type', event_type)
            
            response = db_query.execute()
            results = response.data if response.data else []
            
            # Filter by query
            if query:
                query_lower = query.lower()
                results = [
                    r for r in results
                    if query_lower in r.get('event_type', '').lower() or
                       query_lower in r.get('ip_address', '').lower()
                ]
            
            results.sort(key=lambda x: x['created_at'], reverse=True)
            
            return results
            
        except Exception as e:
            print(f"Error searching security events: {e}")
            return []
    
    def advanced_search(
        self,
        username: str,
        search_params: Dict[str, Any]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Perform advanced search across multiple data types
        
        Args:
            username: Username to search for
            search_params: {
                'query': str,
                'search_in': ['files', 'activity', 'security'],
                'date_from': str (ISO format),
                'date_to': str (ISO format),
                'action_type': str,
                'event_type': str
            }
        
        Returns:
            Dict with results for each search type
        """
        query = search_params.get('query', '')
        search_in = search_params.get('search_in', ['files', 'activity'])
        
        filters = {
            'date_from': search_params.get('date_from'),
            'date_to': search_params.get('date_to'),
            'action_type': search_params.get('action_type')
        }
        
        results = {}
        
        if 'files' in search_in:
            results['files'] = self.search_files(username, query, filters)
        
        if 'activity' in search_in:
            results['activity'] = self.search_activity(username, query, filters)
        
        if 'security' in search_in:
            event_type = search_params.get('event_type')
            results['security'] = self.search_security_events(username, query, event_type)
        
        return results
    
    def get_search_suggestions(self, username: str, partial_query: str) -> List[str]:
        """Get search suggestions based on partial query"""
        try:
            # Get recent filenames
            response = self.client.table('file_history')\
                .select('filename')\
                .eq('username', username)\
                .order('created_at', desc=True)\
                .limit(100)\
                .execute()
            
            filenames = [
                r['filename'] for r in (response.data or [])
                if r.get('filename')
            ]
            
            # Filter by partial query
            if partial_query:
                query_lower = partial_query.lower()
                filenames = [
                    f for f in filenames
                    if query_lower in f.lower()
                ]
            
            # Remove duplicates and limit
            suggestions = list(set(filenames))[:10]
            suggestions.sort()
            
            return suggestions
            
        except Exception as e:
            print(f"Error getting search suggestions: {e}")
            return []
    
    def search_by_date_range(
        self,
        username: str,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Search activities within a date range"""
        try:
            response = self.client.table('file_history')\
                .select('*')\
                .eq('username', username)\
                .gte('created_at', start_date.isoformat())\
                .lte('created_at', end_date.isoformat())\
                .order('created_at', desc=True)\
                .execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            print(f"Error searching by date range: {e}")
            return []
    
    def search_by_ip(self, username: str, ip_address: str) -> List[Dict[str, Any]]:
        """Search activities by IP address"""
        try:
            response = self.client.table('file_history')\
                .select('*')\
                .eq('username', username)\
                .eq('ip_address', ip_address)\
                .order('created_at', desc=True)\
                .execute()
            
            return response.data if response.data else []
            
        except Exception as e:
            print(f"Error searching by IP: {e}")
            return []
    
    def get_popular_searches(self, username: str) -> List[str]:
        """Get popular/frequent file names"""
        try:
            response = self.client.table('file_history')\
                .select('filename')\
                .eq('username', username)\
                .execute()
            
            filenames = [
                r['filename'] for r in (response.data or [])
                if r.get('filename')
            ]
            
            # Count frequency
            from collections import Counter
            counter = Counter(filenames)
            popular = [name for name, count in counter.most_common(10)]
            
            return popular
            
        except Exception as e:
            print(f"Error getting popular searches: {e}")
            return []


    def _search_files_sqlite(self, username: str, query: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search files using SQLite (fallback)"""
        import sqlite3
        try:
            conn = sqlite3.connect("transfers.db")
            cur = conn.cursor()
            
            sql = "SELECT filename, action, ip, timestamp FROM history WHERE username = ?"
            params = [username]
            
            if filters and filters.get('action_type'):
                sql += " AND action = ?"
                params.append(filters['action_type'])
            
            sql += " ORDER BY id DESC LIMIT 100"
            
            cur.execute(sql, params)
            rows = cur.fetchall()
            conn.close()
            
            results = []
            for row in rows:
                if query and row[0]:
                    if query.lower() in row[0].lower():
                        results.append({
                            'filename': row[0],
                            'action': row[1],
                            'ip_address': row[2],
                            'created_at': row[3]
                        })
                elif not query:
                    results.append({
                        'filename': row[0],
                        'action': row[1],
                        'ip_address': row[2],
                        'created_at': row[3]
                    })
            
            return results
        except Exception as e:
            print(f"Error searching files (SQLite): {e}")
            return []


# Global search service instance
search_service = SearchService()


if __name__ == "__main__":
    print("Search Service module")
    print("Use search_service to perform advanced searches")
