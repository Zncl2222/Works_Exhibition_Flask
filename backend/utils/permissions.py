from rest_framework import permissions
from exceptions import EmailNotVerified


class EmailVerify(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.email_validated:
            return True
        raise EmailNotVerified()
