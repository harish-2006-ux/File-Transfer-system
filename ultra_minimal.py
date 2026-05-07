#!/usr/bin/env python3
"""
Ultra minimal Flask app - no imports from local modules
"""
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>🎉 VaultX is LIVE!</h1><p>Deployment successful on Render!</p>'

@app.route('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port)