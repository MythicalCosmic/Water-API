# exception_handlers.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'ok': False,
            'error_code': None,
            'message': None,
        }

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            custom_response_data['error_code'] = 'BAD_REQUEST'
            custom_response_data['message'] = 'The request could not be understood by the server due to malformed syntax.'
        
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            custom_response_data['error_code'] = 'UNAUTHORIZED'
            custom_response_data['message'] = 'Authentication is required and has failed or has not yet been provided.'
        
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            custom_response_data['error_code'] = 'FORBIDDEN'
            custom_response_data['message'] = 'You do not have permission to access this resource. Or Token is invalid or expired.'  
            
        
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            custom_response_data['error_code'] = 'NOT_FOUND'
            custom_response_data['message'] = 'The requested resource could not be found.'
        
        elif response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            custom_response_data['error_code'] = 'METHOD_NOT_ALLOWED'
            custom_response_data['message'] = 'The HTTP method used is not allowed for this resource.'
        
        elif response.status_code == status.HTTP_409_CONFLICT:
            custom_response_data['error_code'] = 'CONFLICT'
            custom_response_data['message'] = 'The request could not be completed due to a conflict with the current state of the resource.'
        
        elif response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
            custom_response_data['error_code'] = 'UNPROCESSABLE_ENTITY'
            custom_response_data['message'] = 'The request was well-formed but could not be followed due to semantic errors.'
            custom_response_data['details'] = {'field': 'email', 'issue': 'This field must be a valid email address.'}
        
        elif response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            custom_response_data['error_code'] = 'TOO_MANY_REQUESTS'
            custom_response_data['message'] = 'Too many requests have been sent in a given amount of time.'
        
        elif response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            custom_response_data['error_code'] = 'INTERNAL_SERVER_ERROR'
            custom_response_data['message'] = 'The server encountered an internal error and could not complete your request.'
        
        elif response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
            custom_response_data['error_code'] = 'SERVICE_UNAVAILABLE'
            custom_response_data['message'] = 'The server is currently unable to handle the request due to maintenance or overload.'
        
        response.data = custom_response_data

    return response
