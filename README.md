# Z-Vuln-Lab

Z-Vuln-Lab is a collection of intentionally vulnerable, containerized practice labs. Each lab lives on its own branch and is designed to run locally for learning and CTF-style practice.

> These applications deliberately contain exploitable code. Run them only on a local machine or an isolated lab network. Never expose them to the public internet.

## Labs

| Lab | Branch | Start command | Address |
| --- | --- | --- | --- |
| HTTP request smuggling | `http-smuggling-v5` | `docker compose up --build` | <http://localhost:8000> |
| JWT authentication bypass | `jwt-oauth-v4` | `docker compose up --build` | <http://localhost:9000> |
| Middleware header bypass / RCE | `middleware-v2` | `docker compose up --build` | <http://localhost:8080> |
| Pickle deserialization / privilege escalation | `pickle_lab` | `docker compose up --build` | <http://localhost:9000> |
| Container privilege escalation | `privesc-v3` | `docker compose up --build` | SSH `localhost:2222` |
| Server-side template injection | `ssti-v1` | `docker compose up --build` | <http://localhost:8080> |

`intro-page` is a documentation-only branch.

## Quick start

```bash
git clone https://github.com/Zwique/Z_Vuln_Lab.git
cd Z_Vuln_Lab
git switch jwt-oauth-v4
docker compose up --build
```

Read the selected branch's README before experimenting. These labs deliberately contain exploitable code; run them only locally or on an isolated lab network.

Stop a lab with `Ctrl-C`, then run `docker compose down` when finished.

## License

MIT. See [LICENSE](LICENSE).
