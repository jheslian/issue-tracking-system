from rest_framework import serializers
from .models import User, Project, Contributor, Issue, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'last_name', 'first_name']


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type']

    def create(self, validated_data):
        project = Project.objects.create(**validated_data)
        user = self.context['request'].user
        Contributor.objects.create(user=user, project=project, permission='author', role='author')
        return project


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['user', 'permission', 'role']

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        return super().to_representation(instance)


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'tag', 'priority', 'status', 'author', 'assignee', 'created_time']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'issue', 'author', 'description', 'created_time']
