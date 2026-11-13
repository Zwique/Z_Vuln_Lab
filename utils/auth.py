import os
from dotenv import load_dotenv

load_dotenv()

USERS = {
    "admin": os.getenv("ADMIN_PASSWORD", "Adm1n@Backup2024!"),
    "guest": "guest",
}


def check_credentials(username, password):
    return USERS.get(username) == password
