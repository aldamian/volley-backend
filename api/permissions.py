from rest_framework. permissions import SAFE_METHODS, BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication


# Custom permissions for the API
class UserAuthenticatedPermission(BasePermission):
    message = 'You are not authenticated.'

    def has_permission(self, request, view):
        response = JWTAuthentication().authenticate(request)
        if response is not None:
            return True
        return False


class UserAdminPermission(BasePermission):
    message = 'You do not have Admin privileges.'

    def has_permission(self, request, view):
        response = JWTAuthentication().authenticate(request)
        if response is not None:
            user, token = response
            role = token.get('role')
            if role == 'Admin':
                return True
        return False


class UserContentCreatorPermission(BasePermission):
    message = 'You do not have Content Creator privileges.'

    def has_permission(self, request, view):
        response = JWTAuthentication().authenticate(request)
        if response is not None:
            user, token = response
            role = token.get('role')
            if role == 'Content Creator':
                return True
        return False
