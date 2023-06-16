from core.models import Comment, M2mUser, Post, Subreddit
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "id")


class M2mUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = M2mUser
        fields = "__all__"

class SubredditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subreddit
        fields = "__all__"
        extra_kwargs = {"subs": {"required": False}}

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {"votes": {"required": False}}

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        extra_kwargs = {"votes": {"required": False}}
