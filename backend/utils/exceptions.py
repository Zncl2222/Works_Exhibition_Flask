from rest_framework.exceptions import APIException


class EmailNotVerified(APIException):
    status_code = 400
    detail = 'Please verify your email first.'
    code = 'Email not verified.'

    def __init__(self, message=detail):
        self.detail = message
