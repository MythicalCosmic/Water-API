from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 15

class CustomPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        current_page = self.page.number
        total_pages = self.page.paginator.num_pages
        page_size = self.get_page_size(self.request)
        total_items = self.page.paginator.count

        return Response({
            'meta': {
                'total': total_items,
                'per_page': page_size,
                'current_page': current_page,
                'last_page': total_pages,
                'first_page_url': self.request.build_absolute_uri(f'?page=1&page_size={page_size}'),
                'last_page_url': self.request.build_absolute_uri(f'?page={total_pages}&page_size={page_size}'),
                'next_page_url': self.get_next_link(),
                'prev_page_url': self.get_previous_link(),
                'path': self.request.build_absolute_uri().split('?')[0],
                'from': (current_page - 1) * page_size + 1 if total_items > 0 else 0,
                'to': min(current_page * page_size, total_items),
            },
            'data': data
        })