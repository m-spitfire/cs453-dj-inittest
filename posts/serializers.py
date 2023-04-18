from rest_framework import serializers

from .models import Post


class PostAdminSerializer(serializers.ModelSerializer):
    """Post admin serializer for post viewset."""

    class Meta:
        """Meta class for the serializer."""

        model = Post
        fields = ["id", "author", "content", "title", "created_at"]


class PostUserSerializer(serializers.ModelSerializer):
    """Post user serializer for user's posts viewset."""

    class Meta:
        """Meta class for the serializer."""

        model = Post
        fields = ["id", "author", "content", "title", "created_at"]
        read_only_fields = ('author',)
