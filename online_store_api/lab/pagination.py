from rest_framework.pagination import PageNumberPagination

class BookPagination(PageNumberPagination):
    page_size = 5       # Default number of items per page
    page_size_query_param = 'size' # Client can override ?size=10 
    max_page_size = 50   # Prevent abuse (too large)


