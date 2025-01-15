from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_mapping = {
            status.HTTP_400_BAD_REQUEST: {
                'error_code': 'BAD_REQUEST',
                'message': 'The request could not be understood by the server due to malformed syntax.',
            },
            status.HTTP_401_UNAUTHORIZED: {
                'error_code': 'UNAUTHORIZED',
                'message': 'Authentication is required and has failed or has not yet been provided.',
            },
            status.HTTP_403_FORBIDDEN: {
                'error_code': 'FORBIDDEN',
                'message': 'You do not have permission to access this resource. Or Token is invalid or expired.',
            },
            status.HTTP_404_NOT_FOUND: {
                'error_code': 'NOT_FOUND',
                'message': 'The requested resource could not be found.',
            },
            status.HTTP_405_METHOD_NOT_ALLOWED: {
                'error_code': 'METHOD_NOT_ALLOWED',
                'message': 'The HTTP method used is not allowed for this resource.',
            },
            status.HTTP_409_CONFLICT: {
                'error_code': 'CONFLICT',
                'message': 'The request could not be completed due to a conflict with the current state of the resource.',
            },
            status.HTTP_422_UNPROCESSABLE_ENTITY: {
                'error_code': 'UNPROCESSABLE_ENTITY',
                'message': 'The request was well-formed but could not be followed due to semantic errors.',
                'details': {'field': 'email', 'issue': 'This field must be a valid email address.'},
            },
            status.HTTP_429_TOO_MANY_REQUESTS: {
                'error_code': 'TOO_MANY_REQUESTS',
                'message': 'Too many requests have been sent in a given amount of time.',
            },
            status.HTTP_500_INTERNAL_SERVER_ERROR: {
                'error_code': 'INTERNAL_SERVER_ERROR',
                'message': 'The server encountered an internal error and could not complete your request.',
            },
            status.HTTP_503_SERVICE_UNAVAILABLE: {
                'error_code': 'SERVICE_UNAVAILABLE',
                'message': 'The server is currently unable to handle the request due to maintenance or overload.',
            },
        }
        error_details = error_mapping.get(
            response.status_code,
            {
                'error_code': 'UNKNOWN_ERROR',
                'message': 'An unexpected error occurred.',
            }
        )
        custom_response_data = {
            'ok': False,
            **error_details
        }

        response.data = custom_response_data

    return response
