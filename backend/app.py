#!/usr/bin/env python3
"""
Vulnerable Backend Service
WARNING: This code contains intentional vulnerabilities for educational purposes
DO NOT use in production!
"""

from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "service": "Internal Backup Service",
        "version": "1.0",
        "endpoints": [
            "/health",
            "/backup"
        ]
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/backup', methods=['POST'])
def backup():
    """
    Backup endpoint - creates backup of specified directory
    
    Expected JSON:
    {
        "path": "/path/to/backup",
        "destination": "/backup/location"
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    path = data.get('path', '/var/log')
    destination = data.get('destination', '/tmp/backup')
    
    # Basic input validation (appears secure but isn't)
    if '..' in path or '..' in destination:
        return jsonify({"error": "Path traversal detected"}), 400
    
    if ';' in path or '&' in destination:
        return jsonify({"error": "Invalid characters detected"}), 400
    
    # VULNERABILITY: Command injection still possible despite "validation"
    # Multiple attack vectors exist:
    # 1. Shell metacharacters in destination after .tar.gz
    # 2. Newline injection
    # 3. Command substitution $() or ``
    # 4. Pipe operator |
    # 5. The app runs as ROOT (major misconfiguration!)
    
    command = f"tar -czf {destination}.tar.gz {path}"
    
    try:
        result = subprocess.run(
            command,
            shell=True,  # DANGEROUS: shell=True with user input
            capture_output=True,
            text=True,
            timeout=5
        )
        
        return jsonify({
            "success": True,
            "message": f"Backup created: {destination}.tar.gz",
            "output": result.stdout
        })
    
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Backup operation timed out"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Running on localhost only - must port forward to access
    app.run(host='127.0.0.1', port=5000, debug=False)