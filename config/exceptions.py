from django.shortcuts import redirect
from rest_framework.views import exception_handler


def auth_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    return redirect('user-login-form')