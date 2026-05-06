#!/usr/bin/env python3
"""
Absolute minimal Flask app for Render testing
"""
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return '''
    <h1>🎉 VaultX Deployment Test SUCCESS!</h1>
    <p>If you see this, Render is working correctly.</p>
    <p>Port: {}</p>
    <p>Environment variables:</p>
    <ul>
        <li>PORT: {}</li>
        <li>SECRET_KEY: {}</li>
        <li>SENDER_EMAIL: {}</li>
    </ul>
    '''.format(
        os.getenv('PORT', 'Not set'),
        os.getenv('PORT', 'Not set'), 
        'Set' if os.getenv('SECRET_KEY') else 'Not set',
        'Set' if os.getenv('SENDER_EMAIL') else 'Not set'
    )

@app.route('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    print(f"Starting app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)