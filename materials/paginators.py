from rest_framework.pagination import PageNumberPagination


class MaterialsPagination(PageNumberPagination):
    """Пагинация для материалов (курсов и уроков)"""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50