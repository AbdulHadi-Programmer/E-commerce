# Lesson: Custom Validation in DRF Serializers 

1. Field-Level Validation 
for a single field 
Example: ensure price >= 1

```python
# Field-level Validation 
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    def validate_price(self, value):
        if value < 1:
            raise serializers.ValidationError("Price must be at least 1")
        return value
```

2. Object-level Validation
For conditions that depends on multiple fields 
Example: discount_price < price 
```pythone
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

    # Object-level validation
    def validate(self, data):
        price = data.get("price")
        discount_price = data.get("discount_price")
        if discount_price and discount_price >= price:
            raise serializers.ValidationError("Discount price must be less than price")
        return data

```

### 🎯 Your Task (Practice)

1. Add a field age to your Customer model (IntegerField).

2. Update your CustomerSerializer:
  - Write a field-level validation so `age >= 18`.
 
3. Add a field discount_price to Product model (DecimalField, nullable).

4. Update your ProductSerializer:
  - Add object-level validation so `discount_price < price`.

  🧩 What the List Covers (and Why It’s Enough)
  | Category                     | Concepts Covered                                                       | Why It’s Critical                                         |
| ---------------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------- |
| **Core DRF Mechanics**       | APIView, ViewSet, Mixins, Serializers, Routers, Permissions, Auth      | Covers 90% of API scaffolding and CRUD design.            |
| **Database & ORM**           | Query optimization, custom managers, transactions, PostgreSQL features | Makes you *database fluent* — key to performance.         |
| **Architecture & Structure** | Service layers, signals, Celery, caching, testing                      | Separates you from junior devs who dump logic into views. |
| **Security & Scalability**   | JWT, permissions, throttling, middleware, Docker                       | Prepares you for real-world production deployments.       |
| **Performance**              | `select_related`, caching, async, Redis, rate limits                   | Lets you handle high traffic without breaking.            |
| **Deployment & Maintenance** | Nginx, Gunicorn, Docker, .env configs                                  | Moves you from “developer” → “engineer”.                  |
| **API Design & Docs**        | REST design, Swagger, versioning                                       | Makes your APIs usable, maintainable, and future-proof.   |


Gpt as you know that my 60 days to become python backend developer challenge is continue today is day 8 and i want you to create a html that because show my roadmap with days duration and tech stack as well as i can tell you in framework currently learned drf basic moving forward to intermediate and then it should be complete in some days from day 8 and then we can learn postrgesql and then fast api and then celery redis and docker etc as i thing you have to keep in mind that is after 2 weeks mean from today my mid term will start and continue till 1.5 week of time and at time we will add things like docker or redis celery because we have to keep all thing light weight and first discuss with me how and what you can add data so i can check and give you correction then go create it .