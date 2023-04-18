from django.db.models.query import QuerySet
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response

from .models import Post
from .serializers import PostAdminSerializer, PostUserSerializer


class PostViewSet(viewsets.ModelViewSet):
    """Admin endpoint for posts."""

    queryset = Post.objects.all().order_by("-created_at")
    serializer_class = PostAdminSerializer
    permission_classes = [permissions.IsAdminUser]


class UserPostsViewSet(viewsets.ModelViewSet):
    """User endpoint for posts."""

    serializer_class = PostUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet:
        """Get the queryset based on request user."""
        return self.request.user.posts.all()

    def create(self, request):
        serializer = PostUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['author'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
