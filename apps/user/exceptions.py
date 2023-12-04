from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import defaults
from rest_framework.views import exception_handler


def permission_denied_view(request, exception=None):
    print(request.data)
    print('v')
    return HttpResponse("Error handler content", status=403)
    #return defaults.permission_denied(request, PermissionDenied, template_name='views/index.html')
    #raise redirect('user-login-form')


def custom_exception_handler(exc, context):
    print('b')
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    #response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    #if response is not None:
   #     response.data['status_code'] = response.status_code

    return redirect('user-login-form')