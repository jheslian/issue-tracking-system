from rest_framework.permissions import BasePermission
from rest_framework import status
from rest_framework.exceptions import APIException
from django.shortcuts import get_object_or_404
from .models import Contributor


class UserActions(BasePermission):
    """ User permission for the comments section
        - user can only retrieve and create comments

    Returns:
        boolean: True grants permission otherwise it's forbidden
    """
    message = 'Permission denied. Your not allowed to perform this action'
    def has_permission(self, request, view):
        user = get_object_or_404(Contributor, user=request.user)
        if user.permission == 'contributor' and (request.method == 'DELETE' or
                                                 request.method == 'UPDATE' or
                                                 request.method == 'PATCH'):
            return False
        """try:
            user = get_object_or_404(Contributor, user=request.user)
            print("in", user)
            if user.permission == 'contributor' and (request.method == 'DELETE' or
                                                     request.method == 'UPDATE' or
                                                     request.method == 'PATCH'):
                return False
        except Contributor.DoesNotExist:

            return False"""
        return True


class IsInProject(BasePermission):
    """ This checks is user is currently in a project

    Returns:
        boolean: True grants permission to access other wise it's forbidden
    """
    message = 'Permission denied. You do not have access on this project.'

    def has_permission(self, request, view,):
        try:
            project_id = view.kwargs.get('project_id')
            instance = Contributor.objects.get( project_id=project_id, user=request.user)
            if instance:
                return True
        except Contributor.DoesNotExist:
            return False
        return True

