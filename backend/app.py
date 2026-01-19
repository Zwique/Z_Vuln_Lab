#!/usr/bin/env python3
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
    
    if '..' in path or '..' in destination:
        return jsonify({"error": "Path traversal detected"}), 400
    
    if ';' in path or '&' in destination:
        return jsonify({"error": "Invalid characters detected"}), 400
    
    command = f"tar -czf {destination}.tar.gz {path}"
    
    try:
        result = subprocess.run(
            command,
            shell=True, # I guess it's fine.
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
    app.run(host='127.0.0.1', port=5000, debug=False)