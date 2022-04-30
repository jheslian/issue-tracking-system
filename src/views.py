from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import logout
from .serializer import RegisterUserSerializer, ProjectSerializer, ContributorSerializer, IssueSerializer, \
    CommentSerializer
from django.contrib.auth import get_user_model
from .models import User, Project, Contributor, Comment, Issue
from .permission import CustomPermission
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from django.shortcuts import get_object_or_404

User = get_user_model()

# Create your views here.

class RegisterUser(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    http_method_names = ['post', ]

@api_view(['GET'])
#@permission_classes([IsAuthenticated])
def User_logout(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully')


class MultipleFieldLookupMixin(object):
    def get_object(self):
        queryset = self.get_queryset()

        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:

            if self.kwargs.get(field, None):
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class ProjectView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ContributorView(generics.ListCreateAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        project_id = self.kwargs['pk']
        return self.queryset.filter(project=project_id)

    def perform_create(self, serializer):
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        return serializer.save(project=project)


class ContributorDetailView(MultipleFieldLookupMixin, generics.RetrieveDestroyAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    lookup_fields = ['project_id', 'user_id']


class IssueView(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_queryset(self):
        project_id = self.kwargs['pk']
        return self.queryset.filter(project=project_id)

    def perform_create(self, serializer):
        project = get_object_or_404(Project, id=self.kwargs['pk'])
        return serializer.save(project=project)


class IssueDetailView(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    lookup_fields = ['project_id', 'id']


class CommentsView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'issue_id'

    def get_queryset(self):
        issue_id = self.kwargs['issue_id']
        return self.queryset.filter(issue=issue_id)

    def perform_create(self, serializer):
        issue = get_object_or_404(Issue, id=self.kwargs['issue_id'])
        return serializer.save(issue=issue)


class CommentDetailView(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_fields = ['issue_id', 'id']
