from flask import Flask, request, jsonify
import os
from auth import create_token, verify_token
from oauth import process_oauth_login

app = Flask(__name__)

USERS = {
    "player": {"password": "player", "role": "user"},
    "admin": {"password": "admin123", "role": "admin"},
}

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = USERS.get(data.get("username"))

    if user and user["password"] == data.get("password"):
        token = create_token(data["username"], user["role"])
        return jsonify({"token": token})

    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/oauth-login", methods=["POST"])
def oauth_login():
    oauth_data = request.json  # attacker-controlled
    user = process_oauth_login(oauth_data)
    token = create_token(user["user"], user["role"])
    return jsonify({"token": token})


@app.route("/profile")
def profile():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    data = verify_token(token)

    if not data:
        return jsonify({"error": "Invalid token"}), 403

    return jsonify(data)


@app.route("/admin")
def admin_panel():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    data = verify_token(token)

    if not data or data.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    return jsonify({"message": "Welcome admin!"})


@app.route("/admin/debug")
def debug():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    data = verify_token(token)

    if not data or data.get("role") != "admin":
        return jsonify({"error": "Admins only"}), 403

    cmd = request.args.get("cmd")
    return os.popen(cmd).read()  # 🔥 RCE


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
