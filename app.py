import os
import redis
from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from dotenv import load_dotenv
from utils.auth import check_credentials
from utils.session import export_session, import_session

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback-dev-key")

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)


@app.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if check_credentials(username, password):
            session.clear()
            session["username"] = username
            session["role"] = "admin" if username == "admin" else "guest"
            session["authenticated"] = True
            redis_client.set(f"session:{username}:last_login", "now")
            return redirect(url_for("dashboard"))
        error = "Invalid username or password."
    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html", username=session["username"], role=session.get("role"))


@app.route("/export")
def export():
    if "username" not in session:
        return redirect(url_for("login"))
    data = export_session(dict(session))
    return data, 200, {
        "Content-Type": "application/octet-stream",
        "Content-Disposition": 'attachment; filename="session.bak"'
    }


@app.route("/import", methods=["POST"])
def import_bak():
    if "username" not in session:
        return redirect(url_for("login"))
    file = request.files.get("session_file")
    if not file:
        flash("No file uploaded.")
        return redirect(url_for("dashboard"))
    raw = file.read()
    restored = import_session(raw)
    session.update(restored)
    flash("Session restored successfully.")
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
