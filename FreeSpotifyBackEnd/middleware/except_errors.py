from django.http import JsonResponse, HttpRequest
from loguru import logger

class ExceptErrors:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        logger.warning(f"Exception {exception.__class__.__name__} was called!")

        logger.warning(f"Exception {exception.__class__.__name__} was called!")
        error_description = exception.message
        error_name = exception.__class__.__name__

        return JsonResponse({
            "error_description": error_description,
            "error_name": error_name
        })
