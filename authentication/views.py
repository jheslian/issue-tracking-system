from rest_framework import viewsets
from rest_framework.response import Response

from .serializers import RegisterUserSerializer
from src.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from .serializers import MyTokenObtainPairSerializer


class RegisterUser(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response({'success': 'Account has been successfully created.'}, status=201)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
