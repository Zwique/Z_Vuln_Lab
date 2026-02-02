#!/usr/bin/env python3
"""
vulnerable_backend.py

Intentionally vulnerable HTTP backend for request smuggling labs.

Features:
- Serves frontend UI from ../frontend/
- Supports /submit and /admin endpoints
- Parses both Content-Length and Transfer-Encoding: chunked
- Leaves leftover bytes after chunked decoding → request smuggling vulnerability
"""

import socket
import threading
import os

HOST = "0.0.0.0"
PORT = 8000

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

with open(os.path.join(BASE_DIR, "flag.txt"), "r") as f:
    FLAG = f.read().strip()

CRLF = b"\r\n"


def read_until_double_crlf(conn, initial=b""):
    buf = bytearray(initial)
    while b"\r\n\r\n" not in buf:
        data = conn.recv(4096)
        if not data:
            break
        buf.extend(data)
    return bytes(buf)


def parse_headers(header_bytes):
    header_text = header_bytes.decode(errors="ignore")
    lines = header_text.split("\r\n")
    request_line = lines[0]
    headers = {}
    for line in lines[1:]:
        if not line:
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip().lower()] = value.strip()
    return request_line, headers


def decode_chunked_body(conn, leftover=b""):
    buf = bytearray(leftover)
    body = bytearray()

    def read_line():
        while b"\r\n" not in buf:
            data = conn.recv(4096)
            if not data:
                return None
            buf.extend(data)
        idx = buf.index(b"\r\n")
        line = bytes(buf[:idx])
        del buf[:idx + 2]
        return line

    while True:
        line = read_line()
        if line is None:
            break
        try:
            size_hex = line.split(b";", 1)[0].strip()
            chunk_size = int(size_hex, 16)
        except ValueError:
            break

        if chunk_size == 0:
            _ = read_line()  # consume final CRLF
            break

        while len(buf) < chunk_size + 2:
            data = conn.recv(4096)
            if not data:
                break
            buf.extend(data)

        chunk = bytes(buf[:chunk_size])
        body.extend(chunk)
        del buf[:chunk_size + 2]

    return bytes(body), bytes(buf)


def http_response(code, body_bytes, content_type="text/plain"):
    reasons = {
        200: "OK",
        400: "Bad Request",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error",
    }
    reason = reasons.get(code, "OK")
    resp = bytearray()
    resp.extend(f"HTTP/1.1 {code} {reason}\r\n".encode())
    resp.extend(f"Content-Length: {len(body_bytes)}\r\n".encode())
    resp.extend(f"Content-Type: {content_type}\r\n".encode())
    resp.extend(b"Connection: close\r\n")
    resp.extend(b"\r\n")
    resp.extend(body_bytes)
    return bytes(resp)


def load_file(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None


def handle_single_request(request_line, headers, body):
    try:
        method, path, _ = request_line.split(" ", 2)
    except ValueError:
        return http_response(400, b"Bad Request\n")

    path = path.lower()

    # Serve frontend
    if path == "/" and method.upper() == "GET":
        data = load_file(os.path.join(FRONTEND_DIR, "index.html"))
        if data is None:
            return http_response(500, b"Frontend not found\n")
        return http_response(200, data, content_type="text/html")

    if path == "/admin" and method.upper() == "GET":
        # Backend-protected admin endpoint (real flag lives here)
        if headers.get("x-admin", "").lower() == "true":
            return http_response(200, FLAG.encode() + b"\n")
        else:
            return http_response(403, b"Forbidden\n")

    if path == "/submit" and method.upper() == "POST":
        return http_response(200, b"Submitted: " + body[:200] + b"\n")

    return http_response(404, b"Not Found\n")


def client_thread(conn, addr):
    try:
        leftover = b""
        while True:
            header_data = read_until_double_crlf(conn, initial=leftover)
            if not header_data:
                break

            parts = header_data.split(b"\r\n\r\n", 1)
            header_block = parts[0]
            leftover = parts[1] if len(parts) > 1 else b""

            request_line, headers = parse_headers(header_block)

            body = b""
            if "transfer-encoding" in headers and "chunked" in headers["transfer-encoding"].lower():
                body, leftover = decode_chunked_body(conn, leftover)
            elif "content-length" in headers:
                try:
                    length = int(headers["content-length"])
                except ValueError:
                    length = 0

                if len(leftover) >= length:
                    body = leftover[:length]
                    leftover = leftover[length:]
                else:
                    body = bytearray(leftover)
                    need = length - len(leftover)
                    leftover = b""
                    while need > 0:
                        data = conn.recv(4096)
                        if not data:
                            break
                        take = data[:need]
                        body.extend(take)
                        need -= len(take)
                        leftover = data[len(take):] if len(data) > len(take) else b""
                    body = bytes(body)
            else:
                body = b""

            try:
                response = handle_single_request(request_line, headers, body)
            except Exception as e:
                response = http_response(500, f"Server error: {e}".encode())

            conn.sendall(response)

            # Vulnerable behavior: leftover bytes are treated as a new request
            if not leftover:
                break
    finally:
        try:
            conn.close()
        except:
            pass


def main():
    print(f"[+] Starting vulnerable backend on {HOST}:{PORT}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(50)

    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=client_thread, args=(conn, addr), daemon=True)
        t.start()


if __name__ == "__main__":
    main()
