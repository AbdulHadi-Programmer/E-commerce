import time
import json 
from django.http import JsonResponse 
from django.utils.deprecation import MiddlewareMixin  # Don't use for new Code 

class SimpleTimingMiddleware:
    """New-style middleware: __init__ (get response) __call__ """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()                     # before view runs
        response = self.get_response(request)   # call the view (and all later middleware)
        duration = time.time() - start          # after view runs
        response["X-Elapsed-Time"] = f"Hello {duration:.3f}s"  # attach to response
        return response


import json
from django.http import JsonResponse
from .models import Product

class PreOrderStockCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Run only for creating orders
        print(f"[Middleware] Path: {request.path} | Method: {request.method}")
        if request.method == "POST" and request.path.startswith("/api/orders"):
            try:
                data = json.loads(request.body)
            except:
                return JsonResponse({"detail": "Invalid JSON"}, status=400)

            product_id = data.get("product")
            quantity = data.get("quantity", 1)

            if not product_id:
                return JsonResponse({"detail": "Product ID required"}, status=400)

            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                return JsonResponse({"detail": "Product not found"}, status=404)

            if product.stock < quantity:
                return JsonResponse({"detail": "Not enough stock"}, status=400)

        # If everything is fine, go to the next step (view)
        return self.get_response(request)


from django.http import JsonResponse
from django.core.cache import cache
import json

class IdempotencyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only for order creation
        if request.method == "POST" and request.path.startswith("/api/orders"):
            key = request.META.get("HTTP_IDEMPOTENCY_KEY")
            if key:
                cached = cache.get(key)
                if cached:
                    # Already processed once
                    return JsonResponse(cached["data"], status=cached["status"])

                response = self.get_response(request)

                if response.status_code in (200, 201):
                    try:
                        data = json.loads(response.content)
                        cache.set(key, {"status": response.status_code, "data": data}, 3600)
                    except Exception:
                        pass
                return response

        return self.get_response(request)

class MyMiddleware:
    def __init__(self, get_response):
        self.get_response= get_response 

    def __call__(self, request):
        # Code before view
        print(f"[Request] {request.method} {request.path}")
        response = self.get_response(request)
        return response
# → You’ll see every request show up in console.

## 15 November 2025:
## Task 1  :
import uuid

class CorrelationID:
    def __init__(self, get_response):
        self.get_response =  get_response

    def __call__(self, request):
        token = uuid.uuid4()  # Create random UUID
        request.correlation_id = token  # Attach it to the request object 
        response = self.get_response(request)   # Process View 
        response["X-Correlation-ID"] = str(token)     # Add Header to response 
        return response



## Task 2 --- Block Requests Based on HTTP Method:
from django.http import HttpResponseNotAllowed
class BlockPostMiddleware :
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST":
            return HttpResponseNotAllowed(["GET", "PUT", "DELETE"])
        response = self.get_response(request)
        return response
     

## Task 3 -- Count Requests pet Path
class PathCounterMiddleware:
    counter = {}
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # logic before view
        path = request.path   # Extract the path
        PathCounterMiddleware.counter[path] = PathCounterMiddleware.counter.get(path, 0) + 1    # Update Dictionary 
        count = PathCounterMiddleware.counter[path]            # Count value 
        # Logic After View
        response = self.get_response(request)
        response["X-Path-Count"] = str(count)
        print(f"X-Path-Count: {count}")

        return response 


