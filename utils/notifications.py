"""
Enhanced Email Notification System
Comprehensive email alerts for all user activities
"""

import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from datetime import datetime
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class EmailNotificationService:
    """Handle all email notifications"""
    
    def __init__(self):
        self.sender_email = os.getenv('SENDER_EMAIL', 'noreply@vaultx.com')
        self.sender_password = os.getenv('SENDER_PASSWORD')
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
    
    def _send_email(self, to_email: str, subject: str, html_body: str, text_body: str) -> bool:
        """Send email with HTML and text fallback"""
        try:
            if not self.sender_password:
                print("Email credentials not configured")
                return False
            
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"VaultX Security <{self.sender_email}>"
            msg['To'] = to_email
            
            # Attach text and HTML versions
            part1 = MIMEText(text_body, 'plain')
            part2 = MIMEText(html_body, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_login_notification(
        self,
        email: str,
        username: str,
        ip: str,
        location: Dict[str, Any],
        device: str,
        timestamp: Optional[datetime] = None
    ) -> bool:
        """Send login notification"""
        if timestamp is None:
            timestamp = datetime.now()
        
        time_str = timestamp.strftime("%B %d, %Y at %I:%M %p")
        location_str = f"{location.get('city', 'Unknown')}, {location.get('country', 'Unknown')}"
        
        subject = "🔐 New Login to Your VaultX Account"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                    <h1 style="color: white; margin: 0;">🔐 VaultX Security Alert</h1>
                </div>
                
                <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #667eea;">New Login Detected</h2>
                    
                    <p>Hi <strong>{username}</strong>,</p>
                    
                    <p>We detected a new login to your VaultX account:</p>
                    
                    <div style="background: #f0f4ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <p style="margin: 5px 0;"><strong>📅 Time:</strong> {time_str}</p>
                        <p style="margin: 5px 0;"><strong>📍 Location:</strong> {location_str}</p>
                        <p style="margin: 5px 0;"><strong>🌐 IP Address:</strong> {ip}</p>
                        <p style="margin: 5px 0;"><strong>💻 Device:</strong> {device}</p>
                    </div>
                    
                    <p><strong>Was this you?</strong></p>
                    <p>If you recognize this activity, you can safely ignore this email.</p>
                    
                    <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0;">
                        <p style="margin: 0;"><strong>⚠️ If this wasn't you:</strong></p>
                        <p style="margin: 5px 0 0 0;">Please change your password immediately and contact support.</p>
                    </div>
                    
                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                    
                    <p style="font-size: 12px; color: #666;">
                        This is an automated security notification from VaultX.<br>
                        For security reasons, please do not reply to this email.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
VaultX Security Alert - New Login Detected

Hi {username},

We detected a new login to your VaultX account:

Time: {time_str}
Location: {location_str}
IP Address: {ip}
Device: {device}

Was this you?
If you recognize this activity, you can safely ignore this email.

⚠️ If this wasn't you:
Please change your password immediately and contact support.

---
This is an automated security notification from VaultX.
        """
        
        return self._send_email(email, subject, html_body, text_body)
    
    def send_suspicious_login_alert(
        self,
        email: str,
        username: str,
        ip: str,
        reasons: list,
        timestamp: Optional[datetime] = None
    ) -> bool:
        """Send suspicious login alert"""
        if timestamp is None:
            timestamp = datetime.now()
        
        time_str = timestamp.strftime("%B %d, %Y at %I:%M %p")
        reasons_html = "".join([f"<li>{reason}</li>" for reason in reasons])
        reasons_text = "\n".join([f"  • {reason}" for reason in reasons])
        
        subject = "🚨 SUSPICIOUS LOGIN ATTEMPT - VaultX Security Alert"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;">
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                    <h1 style="color: white; margin: 0;">🚨 SECURITY ALERT</h1>
                </div>
                
                <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #f5576c;">Suspicious Login Attempt Detected</h2>
                    
                    <p>Hi <strong>{username}</strong>,</p>
                    
                    <div style="background: #ffe6e6; border-left: 4px solid #f5576c; padding: 15px; margin: 20px 0;">
                        <p style="margin: 0;"><strong>⚠️ We detected unusual activity on your account!</strong></p>
                    </div>
                    
                    <p><strong>Suspicious Activity Details:</strong></p>
                    
                    <div style="background: #f0f4ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <p style="margin: 5px 0;"><strong>📅 Time:</strong> {time_str}</p>
                        <p style="margin: 5px 0;"><strong>🌐 IP Address:</strong> {ip}</p>
                        <p style="margin: 10px 0 5px 0;"><strong>🔍 Reasons for Alert:</strong></p>
                        <ul style="margin: 5px 0;">
                            {reasons_html}
                        </ul>
                    </div>
                    
                    <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0;">
                        <p style="margin: 0;"><strong>🛡️ Recommended Actions:</strong></p>
                        <ol style="margin: 10px 0 0 0; padding-left: 20px;">
                            <li>Change your password immediately</li>
                            <li>Review your recent account activity</li>
                            <li>Enable two-factor authentication if not already enabled</li>
                            <li>Contact support if you don't recognize this activity</li>
                        </ol>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://127.0.0.1:8000/profile" style="background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                            Review Account Activity
                        </a>
                    </div>
                    
                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                    
                    <p style="font-size: 12px; color: #666;">
                        This is an automated security notification from VaultX.<br>
                        If you need assistance, please contact our support team.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
🚨 VaultX SECURITY ALERT - Suspicious Login Attempt

Hi {username},

⚠️ We detected unusual activity on your account!

Suspicious Activity Details:
Time: {time_str}
IP Address: {ip}

Reasons for Alert:
{reasons_text}

🛡️ Recommended Actions:
  1. Change your password immediately
  2. Review your recent account activity
  3. Enable two-factor authentication if not already enabled
  4. Contact support if you don't recognize this activity

---
This is an automated security notification from VaultX.
        """
        
        return self._send_email(email, subject, html_body, text_body)
    
    def send_file_upload_notification(
        self,
        email: str,
        username: str,
        filename: str,
        filesize: str,
        timestamp: Optional[datetime] = None
    ) -> bool:
        """Send file upload notification"""
        if timestamp is None:
            timestamp = datetime.now()
        
        time_str = timestamp.strftime("%B %d, %Y at %I:%M %p")
        
        subject = "📁 File Uploaded Successfully - VaultX"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                    <h1 style="color: white; margin: 0;">📁 VaultX File Upload</h1>
                </div>
                
                <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #667eea;">File Uploaded Successfully</h2>
                    
                    <p>Hi <strong>{username}</strong>,</p>
                    
                    <p>Your file has been securely uploaded and encrypted:</p>
                    
                    <div style="background: #f0f4ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <p style="margin: 5px 0;"><strong>📄 Filename:</strong> {filename}</p>
                        <p style="margin: 5px 0;"><strong>📊 Size:</strong> {filesize}</p>
                        <p style="margin: 5px 0;"><strong>📅 Uploaded:</strong> {time_str}</p>
                        <p style="margin: 5px 0;"><strong>🔐 Status:</strong> <span style="color: #28a745;">Encrypted & Secure</span></p>
                    </div>
                    
                    <div style="background: #d4edda; border-left: 4px solid #28a745; padding: 15px; margin: 20px 0;">
                        <p style="margin: 0;">✅ Your file is protected with AES-256 encryption</p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://127.0.0.1:8000/" style="background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                            View My Files
                        </a>
                    </div>
                    
                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                    
                    <p style="font-size: 12px; color: #666;">
                        This is an automated notification from VaultX.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
VaultX - File Uploaded Successfully

Hi {username},

Your file has been securely uploaded and encrypted:

Filename: {filename}
Size: {filesize}
Uploaded: {time_str}
Status: Encrypted & Secure

✅ Your file is protected with AES-256 encryption

View your files at: http://127.0.0.1:8000/

---
This is an automated notification from VaultX.
        """
        
        return self._send_email(email, subject, html_body, text_body)
    
    def send_daily_activity_summary(
        self,
        email: str,
        username: str,
        stats: Dict[str, Any]
    ) -> bool:
        """Send daily activity summary"""
        subject = "📊 Your Daily VaultX Activity Summary"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f9f9f9;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
                    <h1 style="color: white; margin: 0;">📊 Daily Activity Summary</h1>
                </div>
                
                <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h2 style="color: #667eea;">Your VaultX Activity Today</h2>
                    
                    <p>Hi <strong>{username}</strong>,</p>
                    
                    <p>Here's a summary of your activity today:</p>
                    
                    <div style="background: #f0f4ff; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <p style="margin: 5px 0;"><strong>📤 Files Uploaded:</strong> {stats.get('uploads', 0)}</p>
                        <p style="margin: 5px 0;"><strong>📥 Files Downloaded:</strong> {stats.get('downloads', 0)}</p>
                        <p style="margin: 5px 0;"><strong>🗑️ Files Deleted:</strong> {stats.get('deletes', 0)}</p>
                        <p style="margin: 5px 0;"><strong>🔐 Login Count:</strong> {stats.get('logins', 0)}</p>
                        <p style="margin: 5px 0;"><strong>📁 Total Files:</strong> {stats.get('total_files', 0)}</p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://127.0.0.1:8000/profile" style="background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                            View Full Activity
                        </a>
                    </div>
                    
                    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                    
                    <p style="font-size: 12px; color: #666;">
                        This is an automated daily summary from VaultX.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
VaultX - Daily Activity Summary

Hi {username},

Here's a summary of your activity today:

Files Uploaded: {stats.get('uploads', 0)}
Files Downloaded: {stats.get('downloads', 0)}
Files Deleted: {stats.get('deletes', 0)}
Login Count: {stats.get('logins', 0)}
Total Files: {stats.get('total_files', 0)}

View full activity at: http://127.0.0.1:8000/profile

---
This is an automated daily summary from VaultX.
        """
        
        return self._send_email(email, subject, html_body, text_body)


# Global notification service instance
notification_service = EmailNotificationService()


if __name__ == "__main__":
    # Test notifications
    service = EmailNotificationService()
    
    print("Testing email notification system...")
    print("Note: Configure SENDER_EMAIL and SENDER_PASSWORD in .env to test")
