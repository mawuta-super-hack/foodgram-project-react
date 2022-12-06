from rest_framework.pagination import PageNumberPagination


class PageNumberPaginationWithLimit(PageNumberPagination):
    """Класс для пагинации страниц."""

    page_size = 6
    page_size_query_param = 'limit'
