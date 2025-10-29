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

