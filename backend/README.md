# Internal Backup Service

A simple Flask-based backup service for internal use.

## Overview

This service provides REST API endpoints to create backups of system directories.

## Security Features

✅ Path traversal protection (`..` detection)  
✅ Basic input validation (`;` and `&` filtering)  
✅ Timeout protection (5 second limit)  
✅ Runs with minimal required privileges

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

## Deployment Notes

- Service configured to run as systemd service
- Runs with root privileges for backup operations (required for system-wide backups)
- Only accessible from localhost for security
- Input validation prevents common injection attacks

## Security Audit (2024-Q4)

Last security review: October 2024  
Status: ✅ Passed  
Auditor: Internal Security Team

Key findings:
- No SQL injection vectors (no database)
- Path traversal protection working as expected
- Command injection mitigated through input filtering
- Principle of least privilege applied (sudo only for tar)

## TODO

- [ ] Add authentication
- [ ] Add rate limiting
- [ ] Implement backup scheduling
- [ ] Add compression level options