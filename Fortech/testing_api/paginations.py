from rest_framework.pagination import PageNumberPagination


class QuestionAPIPagination(PageNumberPagination):
    """ Пагинация для вывода одного вопроса на странице """
    page_size = 1
    # page_size_query_param = 'page_size'  # Кастомный размер по url-параметру page_size
    # max_page_size = 10  # Максимальное значение кастомного размера
