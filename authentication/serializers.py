from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from src.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    MIN_LENGTH = 8
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password])

    repeat_password = serializers.CharField(
        write_only=True,
        min_length=MIN_LENGTH)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'repeat_password']

    def validate(self, data):
        if data['password'] != data['repeat_password']:
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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims

        return token
