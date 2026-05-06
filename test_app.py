#!/usr/bin/env python3
"""
Minimal test app to verify Render deployment works
"""
from flask import Flask
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'test-key')

@app.route('/')
def home():
    return '''
    <h1>VaultX Test - Deployment Working!</h1>
    <p>If you see this, the Render deployment is successful.</p>
    <p>Environment check:</p>
    <ul>
        <li>SECRET_KEY: {'✅ Set' if os.getenv('SECRET_KEY') else '❌ Missing'}</li>
        <li>SENDER_EMAIL: {'✅ Set' if os.getenv('SENDER_EMAIL') else '❌ Missing'}</li>
        <li>ENCRYPTION_KEY: {'✅ Set' if os.getenv('ENCRYPTION_KEY') else '❌ Missing'}</li>
    </ul>
    '''

@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'VaultX test app is running'}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)