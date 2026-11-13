# Internal Backup Service

A simple Flask-based backup service for internal use.

## Overview

This service provides REST API endpoints to create backups of system directories.

## Claimed Security Features

This section is intentionally misleading challenge content, not a real security review.

- Path traversal protection (`..` detection)
- Basic input validation (`;` and `&` filtering)
- Timeout protection (5 second limit)
- Runs with minimal required privileges

## Endpoints

### GET /
Returns service information and available endpoints.

### GET /health
Health check endpoint.

### POST /backup
Creates a tar.gz backup of a specified directory.

**Request body:**
```json
{
    "path": "/path/to/backup",
    "destination": "/backup/location"
}
```

**Example:**
```bash
curl -X POST http://localhost:5000/backup \
  -H "Content-Type: application/json" \
  -d '{"path": "/var/log", "destination": "/tmp/mybackup"}'
```

## Running the Service

```bash
python3 app.py
```

Service runs on `http://127.0.0.1:5000`

## Actual Deployment Notes

- The container uses Supervisor to start the Flask service
- The Flask service runs as root for this privilege-escalation exercise
- Only accessible from localhost for security
- The blacklist is incomplete and does not prevent command injection

## Deliberately Misleading Audit Text (2024-Q4)

The audit text below is part of the challenge and should not be treated as evidence of security.

Key findings:
- No SQL injection vectors (no database)
- Path traversal protection working as expected
- Command injection appears mitigated through incomplete input filtering
- Least privilege is not applied; the service runs as root

## TODO

- [ ] Add authentication
- [ ] Add rate limiting
- [ ] Implement backup scheduling
- [ ] Add compression level options
