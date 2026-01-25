from flask import Flask, request, render_template, redirect, url_for, make_response
from auth import create_token, decode_token

app = Flask(__name__)

USERS = {
    "player": {"password": "player", "role": "user"},
    "admin": {"password": "supersecretpasswordby_Zwique", "role": "admin"}
}

def get_current_user():
    token = request.cookies.get("token")
    if not token:
        return None
    try:
        return decode_token(token)
    except:
        return None

@app.route("/")
def index():
    user = get_current_user()
    if user:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    user = get_current_user()
    if user:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        data = request.form
        user_data = USERS.get(data["username"])
        if user_data and user_data["password"] == data["password"]:
            token = create_token(data["username"], user_data["role"])
            resp = make_response(redirect(url_for("dashboard")))
            resp.set_cookie("token", token, httponly=True)
            return resp
        return render_template("invalid.html")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=user)

@app.route("/admin")
def admin():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    if user.get("role") != "admin":
        return render_template("error.html"), 403

    with open("flag.txt") as f:
        flag = f.read()
    return render_template("admin.html", flag=flag)

@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("login")))
    resp.set_cookie("token", "", expires=0)
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
