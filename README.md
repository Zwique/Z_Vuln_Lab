# HTTP Request Smuggling Lab

This lab demonstrates a request-parsing mismatch. The intentionally vulnerable server honors `Transfer-Encoding: chunked` and then processes leftover bytes as another request, allowing a hidden `GET /admin` request to follow an innocent-looking submission.

> Run this lab only on localhost or an isolated training network.

## Run it

Requirements: Docker with Compose.

```bash
docker compose up --build
```

Open <http://localhost:8000> to confirm the service is running. Leave the container running while you execute the PoC in another terminal:

```bash
python3 exp.py
```

The PoC prints both HTTP responses. The second response contains the lab flag.

Stop the lab with:

```bash
docker compose down
```

## What to study

The server intentionally combines chunked-body parsing with connection reuse. Compare the first response to `POST /submit` with the second response to the smuggled `GET /admin` request. In a real deployment, a frontend and backend must agree on how to frame requests and must reject ambiguous `Content-Length` plus `Transfer-Encoding` combinations.
