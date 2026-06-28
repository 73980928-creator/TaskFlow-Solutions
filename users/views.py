from django.contrib.auth.models import User
from rest_framework import generics, permissions

from .serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    """Registro de nuevos usuarios. Endpoint publico (no requiere login)."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserListView(generics.ListAPIView):
    """Lista de usuarios (util para asignar tareas)."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
