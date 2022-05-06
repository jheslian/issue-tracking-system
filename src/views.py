from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import ProjectSerializer, ContributorSerializer, IssueSerializer, \
    CommentSerializer
from .models import Project, Contributor, Comment, Issue
from .permission import UserActions, IsInProject
from django.shortcuts import get_object_or_404


class MultipleFieldLookupMixin(object):
    """ This gets the lookup_fields to set multiple filter on a query """

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field, None):
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class ProjectView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': 'Project created.', 'data': request.data}, status=201)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, UserActions]
    lookup_field = 'pk'
    lookup_url_kwarg = 'project_id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": f"Project {instance.title} deleted."}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': "Project updated", 'data': serializer.data})


class ContributorView(generics.ListCreateAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "project_id"

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        obj = Contributor.objects.filter(project_id=project_id)
        users_id = []
        for user in obj:
            users_id.append(user.user.id)

        return self.queryset.filter(project=project_id, user_id__in=users_id)

    def perform_create(self, serializer):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        return serializer.save(project=project)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        project = self.get_object()
        return Response({'success': f'User added in {project}.', 'data': request.data}, status=201)


class ContributorDetailView(MultipleFieldLookupMixin, generics.RetrieveDestroyAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsInProject]
    lookup_fields = ['project_id', 'user_id']

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        self.perform_destroy(user)
        return Response({"message": f"User {user.user.last_name} has been deleted."}, status=201)


class IssueView(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsInProject, UserActions]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return self.queryset.filter(project=project_id)

    def perform_create(self, serializer):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        default_user = self.request.user
        return serializer.save(project=project, assignee=default_user, author=default_user)


class IssueDetailView(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsInProject, UserActions]
    lookup_fields = ['project_id', 'id']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'message': "Issue updated", 'data': serializer.data})

    def destroy(self, request, *args, **kwargs):
        issue = self.get_object()
        self.perform_destroy(issue)
        return Response({"message": f"Issue {issue.title} deleted."}, status=201)


class CommentsView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsInProject, UserActions]
    lookup_field = 'issue_id'

    def get_queryset(self):
        issue_id = self.kwargs['issue_id']
        return self.queryset.filter(issue=issue_id)

    def perform_create(self, serializer):
        issue = get_object_or_404(Issue, pk=self.kwargs['issue_id'])
        return serializer.save(issue=issue, author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'success': f'Comment created.', 'data': serializer.data}, status=status.HTTP_201_CREATED,
                        headers=headers)


class CommentDetailView(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsInProject, UserActions]
    lookup_fields = ['issue_id', 'id']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({'success': f'Comment updated.', 'data': serializer.data})

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        self.perform_destroy(comment)
        return Response({"message": f"Comment '{comment.description}' deleted."}, status=201)
