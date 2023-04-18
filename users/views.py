from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import permissions, viewsets

from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Admin endpoints for users."""

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

