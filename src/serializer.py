from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from .models import User, Project, Contributor, Issue, Comment

MIN_LENGTH = 8


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password])

    password2 = serializers.CharField(
        write_only=True,
        min_length=MIN_LENGTH)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Password does not match")
        return data

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


"""
class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()"""


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ContributorSerializer(serializers.ModelSerializer):
    #user = serializers.SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ['user', 'permission', 'role']

    """def get_user(self, instance):
        queryset = instance.user.all()
        serializer = UserSerializer(queryset , many=True)
        return serializer.data"""


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'contributor']


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ['id','title', 'description', 'tag', 'priority','status', 'author', 'assignee', 'created']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue', 'created']
