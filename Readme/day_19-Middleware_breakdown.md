## Day 19 -- 14 November 2025:

### Middleware (Kid Version + Developer Logic):
Imagine your Django App is a school and every request is a student entering the school. 

Middleware is like the guards and teachers standing in a line at the school gate, checking or modifying the students before they enter and after they leave.

Every request must pass through this chain: 
```sql
Request → M1 → M2 → M3 → ... → View
Response ← M1 ← M2 ← M3 ← ... ← View
```

- Request Phase: Middleware can inspect or modify the request before it reaches your view.
- Response Phase: Middleware can inspect or modify the response before it reaches the client.

That's literally all you need to understand.

## What I actually need to understand: 
- Logging 
- Authentication or Token Extraction 
- Blocking Certain IPs
- Adding custom Headers
- Measuring response time
That's it. 

If you try to learn more than this, you're wasting time.

### Middleware Template I have Must to Memorize :
```py
class Middleware :
    def __init__(self, get_response):
        self.get_response = get_response
        # One time configuration 

    def __call__(self, request):
        # Code that runs BEFORE the view (Process Request)

        response = self.get_response(request)

        # Code that runs AFTER the view (Process Response)

        return response 
```
If you understand this skeleton, you can write any middleware.

#### Explaination Like You're a KID 
`__init__`
This runs ONE Time when Django start the server.
Like a teacher preparing before the students come.

`__call__`
This runs EVERY time a request comes and a response goes.

### Practical Example 1 : Add a Header to Every Response
```py
class AddHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response 
    
    def __call__(self, request):
        response = self.get_response(request)
        response["X-Backend"] = "Django"
        return response 
```
Use Case:
Some Companies add custom headers for debugging, API versioning, etc.

## Practical Example #2: Block a Specific IP
```py
from django.http import HttpResponseForbidden 

class BlockIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        blocked = ["192.168.1.10"]
        ip = request.META.get("REMOTE_ADDR")
        
        if ip in blocked:
            return HttpResponseForbidden("You are Blocked")

        return self.get_response(request)
```
Use Case : 
Basic Security / access control.

## Practical Example #3: Log the Time a View Takes 
```py
import time

class TimerMiddleware :
    def __init__(self, get_response):
        self.get_response = get_response 

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)

        end = time.time()
        print(f"Request took {end - start:.3f} seconds")

        return response 
```
Use Case:
Performance Monitoring.
Companies actually do this.

## How to Enable Middleware (Don't Forget this)
Got to settings.py → add the middleware:
```py
MIDDLEWARE = [
    ...,
    'yourapp.middleware_file.TimerMiddleware',
]
```
If you forget this, your middleware does nothing. 

## Your Quiz :
Write a Middleware that :

1. Print the user's browser info (User-Agent) for every request. 
- You must access `request.META`
- Print it before calling `get_response`
- Return the response normally
```py
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response 
    
    def __call__(self, request):
        user_agent = request.META.get("HTTP_USER_AGENT", "Unknown User Agent")
        print(f"Your Use Agent is: {user_agent}")

        response = self.get_response(request)
        return response
```

2. Add a custom header: `X-Processed-By: AbdulHadiMiddleware`
- Add it to the response
- Return the response 
```py
class MyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Processed-By'] = "AbdulHadiMiddleware"
        return response 
```

3. Block Requests to your API if the path contains `/admin`
- If request.path start with `/admin` , return `HttpResponseForbidden`
- Else continue as normal.
```py
from django.http import HttpResponseForbidden 

class BlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response(request)

    def __call__(self, request):
        if request.path.startswith("/admin"):
            return HttpResponseForbidden("Access to admin is forbidden")
        
        response =self.get_response(request)
        return response
```

# 15 November :
## New Task Set 2 (Realistic for your current level)
These tasks are not tiny, but they are 100% within your skill range if you think clearly.

No databases.
No API keys.
No async.
Only logic + request / response processing.

---

### Task 1 —— Add a Correlation ID to Every Request
What is a correlation ID?
A unique ID added to every request so backend logs can track it.

Your Middleware must:
- Generate a random UUID (use `uuid.uuid4()`)
- Save it to into request.correlation_id
- Add it to the response header:
```md
X-Correlation-ID: <value>
```
**Skills Tested :**
- Before View: Modify request 
- After View: modify response
- Use Python modules

---

### Task 2 —— Block Requests Based on HTTP Method
Write middleware that:
- Blocks every POST request.
- Returns:
```md
405 Method not Allowed
```
- Allows GET/PUT/DELETE normally
**Skills Tested:**
- Accessing `request.method` 
- Conditional Blocking
- Returning an early response

---

### Task 3 —— Count Requests Per Path  (In Memory)
You must create a middleware that tracks how many times each path was accessed.

**Requirements:**
- Use a class-level dictionary:
```py
class PathCounterMiddleware:
    counter = {}
```
- Every time a request comes:
  - Increase counter for that path
- After the response, add this header:
```mathamatica
X-Path-Count: <count>
```

**Skills Tested:**


