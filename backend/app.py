from flask import Flask, request, render_template, redirect, url_for, make_response
from auth import create_token, decode_token

app = Flask(__name__)

USERS = {
    "player": {"password": "player", "role": "user"},
    "admin": {"password": "supersecretpasswordby_Zwique", "role": "admin"}
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        user = USERS.get(data["username"])
        if user and user["password"] == data["password"]:
            token = create_token(data["username"], user["role"])
            resp = make_response(redirect(url_for("dashboard")))
            resp.set_cookie("token", token)
            return resp
        return "Invalid credentials", 403
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    token = request.cookies.get("token")
    if not token:
        return redirect(url_for("login"))

    try:
        payload = decode_token(token)
        return render_template("dashboard.html", user=payload)
    except:
        return "Invalid token", 403

@app.route("/admin")
def admin():
    token = request.cookies.get("token")
    if not token:
        return redirect(url_for("login"))

    try:
        payload = decode_token(token)
        if payload.get("role") != "admin":
            return "Access denied: Admins only", 403

        with open("flag.txt") as f:
            flag = f.read()
        return render_template("admin.html", flag=flag)

    except Exception as e:
        return "Invalid token", 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
