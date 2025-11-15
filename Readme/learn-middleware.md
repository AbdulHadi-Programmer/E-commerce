## 7 November 2025:

### 🧩 Level 1 — Basic anatomy
Learn this minimal pattern first:
```py
class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code before view
        response = self.get_response(request)
        # Code after view
        return response
```
That’s it.

Every middleware you’ll ever write follows this structure.


### 🧩 Level 2 — Intercept and return a custom response
Write one that blocks all requests from a specific IP.
```py
from django.http import JsonResponse

class BlockIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.blocked_ips = ["127.0.0.1"]  # your local IP just for testing

    def __call__(self, request):
        ip = request.META.get("REMOTE_ADDR")
        if ip in self.blocked_ips:
            return JsonResponse({"detail": "Access denied"}, status=403)
        return self.get_response(request)
```
`→ Now you’ve written middleware that can stop requests early.`
That’s the same pattern used by Django’s AuthenticationMiddleware, CSRFMiddleware, etc.

### 🧩 Level 3 — Modify response (like timing or headers)
You already saw `SimpleTimingMiddleware`.
That’s Level 3.
It adds or modifies data after the view has run.

### 