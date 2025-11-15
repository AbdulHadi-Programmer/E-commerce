## 29 October 2029 : 
### Task 1 -- Multi Field Search 
Goal : 
Allow Searching books by title, description, or author bio.
If the user searches "fantasy", it should find both fantasy books and authors whose bio mentions fantasy.

**Hints:**
- Use `Q` lookups accross related fields (author__bio__icontains).
- Combine multiple Q objects with j.
.
---

### Task 2 -- Multi Value Filtering 
Goal:
Allow multiple genres to be filtered at once.
Example:
```sh
/books/?genre=Tech,Education
```
Should return all books whose genre is either Tech or Education.

**Hints:**
- Split the query string by commas:
`genres = request.GET.get('genre').split(',')`
- Use `genre__in=genre`
.
---

### Task 3 - Price Range Filtering 
Goal :
Allow users to filter books within a specific price range.
Example:
```sh
/books/?min_price=10&max_price=25
```
Should show all books priced between $10 and $25 

**Hints:**
Use `price__gte` and `price__lte` filters.
Make sure you check that query params exists before filtering.
.
---

### THE All Above Task could be completed already 

### Task 4 - Advanced Sorting 
Goal :
let the user sort results by an field (price, title, year) with ascending / descending order.
Example: 
```sh
/books/?sort_by=price&order=desc
```
**Hints:**
- Build a dynamic order key:

```python
sort_by = request.GET.get('sort_by', 'created_at')
order = request.GET.get('order', 'asc')
order_key = sort_by if order == 'asc' else f'-{sort_by}'
books = books.order_by(order_key)
```
- Handle invalid fields gracefully (use a whitelists of allowed sort fields).
.
---

### Task 5 - Combine Search  + Filter 
Goal :
Allow combined search and filter queries.
Example:
```sh
/books/?search=python&genre=Tech&year=2024
```
Should find all books in Tech genre, published in 2024, where title/description/author name includes python.
**Hints:**
- Apply filters incrementally, not one giant query.
- Always start from books = Book.objects.all()

### Bonus Model Ideas (For Variety)
Here are two models you can create in a same app to practice similar logic in different contexts.

# Model 1 -Movie
```py
class Movie(models.Model):
    title = models.CharField(max_length=200)
    director = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, default="Drama")
    release_year = models.IntegerField(default=2024)
    rating = models.FloatField(default=5.0)
    duration = models.IntegerField(default=120)  # minutes
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```
**Practice Tasks:**
1. filter by genre + rating range 
2. Search by title or director 
3. Order by rating or release year 
4. filter only movies longer than X minutes 
5. Returns only available movies sorting by newest 

---

### Model 2 - Course 
```py
class Course(models.Model):
    name = models.CharField(max_length=150)
    instructor = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="General")
    duration_weeks = models.PositiveIntegerField(default=4)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    level = models.CharField(max_length=50, default="Beginner")  # Beginner / Intermediate / Advanced
    created_at = models.DateTimeField(auto_now_add=True)

```
**Practice Tasks:**
1. Search courses by name or Instructor
2. Filter by category and level 
3. filter by duration range
4. sort by price or duration 
5. Combine: ?search=python&category=Programming&order=price_desc

**`---------------`**
**` Add Fake DATA `**
**`---------------`**

### Movie Model Data: (Write the logic for below)
🧠 You can test:
* Search by director → `?search=nolan`
* Filter by genre → `?genre=Sci-Fi`
* Filter by rating range → `?min_rating=8&max_rating=9`
* Order by → `?sort_by=rating&order=desc`
* Filter by availability → `?is_available=true`

### Course Model Data: (Write the logic for below ):
🧠 You can test:
* Search → `?search=Python` or `?search=Alice`
* Filter by category → `?category=AI & Data Science`
* Filter by level → `?level=Intermediate`
* Filter by price range → `?min_price=50&max_price=120`
* Order by duration → `?sort_by=duration_weeks&order=desc` 