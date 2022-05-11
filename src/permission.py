from rest_framework.permissions import BasePermission
from .models import Contributor, Issue, Comment


class UserProjectActions(BasePermission):
    """ User permission for the comments section
        - only the outhor of the projects can perform CRUD
        - user contributor can only retrieve and create comments

    Returns:
        boolean: True grants permission otherwise it's forbidden
    """
    message = 'Permission denied. Your not allowed to perform this action'

    def has_permission(self, request, view):

        try:
            user = Contributor.objects.get(project=view.kwargs.get('project_id'), user=request.user)
            if user.permission == 'contributor' and (request.method == 'DELETE' or
                                                     request.method == 'UPDATE' or
                                                     request.method == 'PUT' or
                                                     request.method == 'PATCH'):
                return False

        except Contributor.DoesNotExist:
            return False
        return True


class UserIssueActions(BasePermission):
    """ User permission for the comments section
        - user can only retrieve and create comments

    Returns:
        boolean: True grants permission otherwise it's forbidden
    """
    message = 'Permission denied. Your not allowed to perform this action'

    def has_permission(self, request, view):

        try:
            issue = Issue.objects.get(project=view.kwargs.get('project_id'), id=view.kwargs.get('id'))
            if issue.author != request.user and (request.method == 'DELETE' or
                                                 request.method == 'UPDATE' or
                                                 request.method == 'PUT' or
                                                 request.method == 'PATCH'):
                return False

        except Issue.DoesNotExist:
            self.message = 'Access forbidden or this issue does not exist.'
            return False
        return True


class UserCommentActions(BasePermission):
    """ User author can perform CRUD otherwise create an get is only the option

    Returns:
        boolean: True grants permission otherwise it's forbidden
    """
    message = 'Permission denied. Your not allowed to perform this action'

    def has_permission(self, request, view):
        try:
            issue = Comment.objects.get(issue=view.kwargs.get('issue_id'), id=view.kwargs.get('id'))
            if issue.author != request.user and (request.method == 'DELETE' or
                                                 request.method == 'UPDATE' or
                                                 request.method == 'PUT' or
                                                 request.method == 'PATCH'):
                return False

        except Comment.DoesNotExist:
            self.message = 'Access forbidden or this issue does not exist.'
            return False
        return True


class IsInProject(BasePermission):
    """ This checks if user is currently in this project

    Returns:
        boolean: True grants permission to access other wise it's forbidden
    """
    message = 'Permission denied. You do not have access on this project.'

    def has_permission(self, request, view, ):
        try:
            project_id = view.kwargs.get('project_id')
            instance = Contributor.objects.get(project_id=project_id, user=request.user)
            if instance:
                return True
        except Contributor.DoesNotExist:
            self.message = 'This project does not exist.'
            return False
        return True
