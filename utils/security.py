"""
Advanced Security Utilities
Suspicious login detection, device fingerprinting, geolocation
"""

import hashlib
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import requests
from database.supabase_client import get_supabase, log_file_action


class SecurityMonitor:
    """Monitor and detect suspicious activities"""
    
    def __init__(self):
        self.failed_attempts = {}  # Track failed login attempts
        self.suspicious_ips = set()  # Known suspicious IPs
        self.max_failed_attempts = 5
        self.lockout_duration = timedelta(minutes=15)
    
    def generate_device_fingerprint(self, user_agent: str, ip: str) -> str:
        """Generate unique device fingerprint"""
        fingerprint_data = f"{user_agent}:{ip}"
        return hashlib.sha256(fingerprint_data.encode()).hexdigest()
    
    def get_geolocation(self, ip: str) -> Dict[str, Any]:
        """Get geolocation data for IP address"""
        try:
            # Using ipapi.co for geolocation (free tier)
            response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=3)
            if response.status_code == 200:
                data = response.json()
                return {
                    'country': data.get('country_name', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('region', 'Unknown'),
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude'),
                    'timezone': data.get('timezone', 'Unknown')
                }
        except Exception as e:
            print(f"Geolocation error: {e}")
        
        return {
            'country': 'Unknown',
            'city': 'Unknown',
            'region': 'Unknown',
            'latitude': None,
            'longitude': None,
            'timezone': 'Unknown'
        }
    
    def is_suspicious_login(
        self,
        username: str,
        current_ip: str,
        last_ip: Optional[str],
        user_agent: str,
        last_user_agent: Optional[str]
    ) -> tuple[bool, List[str]]:
        """
        Detect suspicious login attempts
        
        Returns:
            tuple: (is_suspicious, reasons)
        """
        reasons = []
        
        # Check 1: Different IP address
        if last_ip and current_ip != last_ip:
            reasons.append(f"Login from new IP: {current_ip} (previous: {last_ip})")
        
        # Check 2: Different device/browser
        if last_user_agent and user_agent != last_user_agent:
            reasons.append("Login from new device/browser")
        
        # Check 3: Known suspicious IP
        if current_ip in self.suspicious_ips:
            reasons.append(f"Login from known suspicious IP: {current_ip}")
        
        # Check 4: Too many failed attempts
        if self.is_ip_locked_out(current_ip):
            reasons.append(f"Too many failed login attempts from IP: {current_ip}")
        
        # Check 5: Geolocation change (if available)
        if last_ip and current_ip != last_ip:
            current_geo = self.get_geolocation(current_ip)
            last_geo = self.get_geolocation(last_ip)
            
            if current_geo['country'] != last_geo['country']:
                reasons.append(
                    f"Login from different country: {current_geo['country']} "
                    f"(previous: {last_geo['country']})"
                )
        
        return len(reasons) > 0, reasons
    
    def record_failed_attempt(self, ip: str):
        """Record a failed login attempt"""
        if ip not in self.failed_attempts:
            self.failed_attempts[ip] = []
        
        self.failed_attempts[ip].append(datetime.now())
        
        # Clean old attempts (older than lockout duration)
        cutoff = datetime.now() - self.lockout_duration
        self.failed_attempts[ip] = [
            attempt for attempt in self.failed_attempts[ip]
            if attempt > cutoff
        ]
        
        # Add to suspicious IPs if too many attempts
        if len(self.failed_attempts[ip]) >= self.max_failed_attempts:
            self.suspicious_ips.add(ip)
    
    def is_ip_locked_out(self, ip: str) -> bool:
        """Check if IP is locked out due to failed attempts"""
        if ip not in self.failed_attempts:
            return False
        
        cutoff = datetime.now() - self.lockout_duration
        recent_attempts = [
            attempt for attempt in self.failed_attempts[ip]
            if attempt > cutoff
        ]
        
        return len(recent_attempts) >= self.max_failed_attempts
    
    def clear_failed_attempts(self, ip: str):
        """Clear failed attempts for IP (after successful login)"""
        if ip in self.failed_attempts:
            del self.failed_attempts[ip]
        if ip in self.suspicious_ips:
            self.suspicious_ips.remove(ip)
    
    def log_security_event(
        self,
        username: str,
        event_type: str,
        ip: str,
        details: Dict[str, Any]
    ):
        """Log security event to database"""
        try:
            client = get_supabase()
            client.table('security_events').insert({
                'username': username,
                'event_type': event_type,
                'ip_address': ip,
                'details': json.dumps(details),
                'created_at': datetime.now().isoformat()
            }).execute()
        except Exception as e:
            # Silently fail if Supabase not configured - just print to console
            print(f"Security event: {event_type} for {username} from {ip}")
    
    def get_security_events(
        self,
        username: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get recent security events"""
        try:
            client = get_supabase()
            query = client.table('security_events').select('*')
            
            if username:
                query = query.eq('username', username)
            
            response = query.order('created_at', desc=True).limit(limit).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error getting security events: {e}")
            return []


# Global security monitor instance
security_monitor = SecurityMonitor()


def check_password_strength(password: str) -> Dict[str, Any]:
    """
    Check password strength
    
    Returns:
        dict: {
            'score': int (0-4),
            'strength': str,
            'suggestions': list
        }
    """
    score = 0
    suggestions = []
    
    # Length check
    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters")
    
    if len(password) >= 12:
        score += 1
    
    # Complexity checks
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    if has_upper and has_lower:
        score += 1
    else:
        suggestions.append("Use both uppercase and lowercase letters")
    
    if has_digit:
        score += 1
    else:
        suggestions.append("Include at least one number")
    
    if has_special:
        score += 1
    else:
        suggestions.append("Include at least one special character")
    
    # Determine strength
    if score <= 1:
        strength = "Very Weak"
    elif score == 2:
        strength = "Weak"
    elif score == 3:
        strength = "Medium"
    elif score == 4:
        strength = "Strong"
    else:
        strength = "Very Strong"
    
    return {
        'score': score,
        'strength': strength,
        'suggestions': suggestions
    }


def validate_ip_address(ip: str) -> bool:
    """Validate IP address format"""
    try:
        parts = ip.split('.')
        return len(parts) == 4 and all(0 <= int(part) <= 255 for part in parts)
    except:
        return False


if __name__ == "__main__":
    # Test security features
    monitor = SecurityMonitor()
    
    # Test password strength
    print("Testing password strength:")
    passwords = ["weak", "Stronger1", "VeryStr0ng!", "MyP@ssw0rd123!"]
    for pwd in passwords:
        result = check_password_strength(pwd)
        print(f"  {pwd}: {result['strength']} (score: {result['score']})")
    
    # Test suspicious login detection
    print("\nTesting suspicious login detection:")
    is_sus, reasons = monitor.is_suspicious_login(
        "testuser",
        "192.168.1.100",
        "192.168.1.1",
        "Mozilla/5.0",
        "Chrome/90.0"
    )
    print(f"  Suspicious: {is_sus}")
    for reason in reasons:
        print(f"    - {reason}")
