### 15 Novemeber 2025:
## Task 1 —— Time the Request
Write middleware that:
- Captures request start time (before view)
- Captures end time (after view)
- Calculates total processing time in milliseconds
- adds header :
```cs
X-Response-Time: 87ms
```
**Hint:** time.time()
No Further Hints.


## Task 2 —— Only Allow Requests with a custom header 
If the request does NOT have :
```arduino 
X-API-Client: mobile
```
...returns `HttpResponseForbidden("Missing Header")`
Otherwise allow request.
**No hints. Think**

## Task 3 —— Detect Slow Views 
If a request takes more than 0.5 seconds, print:
```pgsql
WARNING: SLOW REQUEST <path> took <time> second
```
Otherwise do nothing.
**This teaches real-world monitoring.**

## Task 4 —— Block Suspicious IPs
If the IP starts with `"192.168."` → block it (forbidden)
Otherwise allow.
**Hint:**
`request.META["REMOTE_ADDR"]`

## Task 5 —— Force JSON Only 
If the request does NOT have header :
```pgsql
Content-Type: application/json
```
→ Block it with HttpResponseUnsupportedMediaType.

## Task 6 —— Add Unique ID to Every Response Body
Not Header — BODY.
If the response is JSON-like (string or JSONResponse):
```json
{"request_id": "<uuid>"}
```
If not JSON response, ignore.

**This is Advanced. Try Anyway.**

## Task 7 —— Count Requests Per IP
Like your path counter, but:
```md
IP: count value
```
Add header:
```md
X-IP-Hit: <count>
```

