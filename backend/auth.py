import datetime

import jwt


SECRET_KEY = "zwiqueishandsome123!"


def create_token(username, role):
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_token(token):
    # Intentionally vulnerable: signature verification is disabled for the lab.
    return jwt.decode(token, SECRET_KEY, options={"verify_signature": False})
