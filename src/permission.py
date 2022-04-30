from rest_framework.permissions import SAFE_METHODS, BasePermission
from .models import Contributor


class CustomPermission(BasePermission):
    message = ""

    def has_permission(self, request, view):
        pass
