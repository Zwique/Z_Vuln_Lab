def process_oauth_login(oauth_data):
    email = oauth_data.get("email")

    # Trusts email only, no issuer or subject validation
    if email == "admin@zvuln.lab":
        return {"user": "admin", "role": "admin"}

    return {"user": email.split("@")[0], "role": "user"}
