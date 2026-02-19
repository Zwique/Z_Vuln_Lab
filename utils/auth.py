import os
from dotenv import load_dotenv

load_dotenv()

USERS = {
    "admin": os.getenv("ADMIN_PASSWORD", "admin123"),
    "guest": "guest",
}


def check_credentials(username, password):
    return USERS.get(username) == password
