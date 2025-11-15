## 7 November 2025: 
### What Middleware really is :
When a client (like your browser or mobile app) sends a request to your server, Django doesnot go straight to your view. The Request passes through a pipeline —— a sequence of small filters called middleware. 

Each middleware can :
- Look at the request before it hits your view.
- Look at or change the response after the views runs. 

That's it.

Think of it like airport security :
- You walk through scanners (middleware 1 checks your bag, 2 checks your passport, 3 checks temperature, etc)
- Then you board your flight (the Django View)
- On your way out, you might pass through exit checks (response phase)

Middleware = gatekeepers for every request.

### Django Request Flow 
```md
Client → Middleware1 → Middleware2 → Middleware3 → View → Middleware3 → Middleware2 → Middleware1 → Client
```
Each middleware can:
- Stop the request early (return its own response).
- Let it pass to the next one.
- Modify the response before it goes back.

### A simple Example —— timing middleware 
Let's say you want to know how long each request takes.
You write this tiny middleware:
```py
import time

class SimpleTimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response  # this gives you access to the next step

    def __call__(self, request):
        start = time.time()                     # before view runs
        response = self.get_response(request)   # call the view (and all later middleware)
        duration = time.time() - start          # after view runs
        response["X-Elapsed-Time"] = f"{duration:.2f}s"  # attach to response
        return response
```

What happens:
1. Every request hits this middleware.
2. It records start time.
3. Lets Django process the request (view runs).
4. Measures how long it took.
5. Adds that info in a response header.
6. Returns it to the client.

→ You didn’t touch any view code, but you added global monitoring to all views.
Tha1t’s the real power of middleware.

### Example from your project — Pre-order stock check 
Let's say users send a request to:
```bash
POST /api/orders/
{
  "product": 5,
  "quantity": 10
}
```
You want to quickly reject request if the product is out of stock before hitting your heavy view logic.

Here's that middleware again in simple words:
```py
import json
from django.http import JsonResponse
from .models import Product

class PreOrderStockCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Run only for creating orders
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
```
### ✅ What happens step-by-step:
1. Client sends POST /api/orders/.
2. This middleware runs before your view.
3. It reads the request body (product, quantity).
4. Checks the database for stock.
5. If stock is low → returns a 400 immediately (skips your whole view).
6. If enough stock → lets the request continue to your OrderViewSet.

So you just added a global “pre-check” without touching your views.


| Use Case                              | Possible Middleware Solution                                               |
| ------------------------------------- | -------------------------------------------------------------------------- |
| User clicks “Place Order” twice       | Idempotency middleware (checks for duplicate key, avoids duplicate insert) |
| Too many identical GETs for same data | Caching middleware (stores and reuses response from cache)                 |
| Too many requests from same IP        | Throttling middleware                                                      |
| Need to log each request globally     | Logging middleware                                                         |
| Measure speed of each request         | Timing middleware                                                          |

