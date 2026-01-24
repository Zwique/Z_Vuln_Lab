import jwt
from datetime import datetime, timedelta

SECRET = "secret"  # Weak secret on purpose

def create_token(username, role):
    payload = {
        "user": username,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def verify_token(token):
    try:
        # 🔥 Accepts alg:none if attacker sets it
        return jwt.decode(token, SECRET, options={"verify_signature": False})
    except Exception:
        return None
