from rest_framework.permissions import AllowAny
from rest_framework import generics

from users.serializers import RegisterSerializer


class CustomUserView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
