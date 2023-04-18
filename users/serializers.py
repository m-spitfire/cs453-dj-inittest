from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(UserDetailsSerializer):
    """User serializer for user viewset."""

    class Meta:
        """Meta class for the serializer."""

        model = User
        fields = ['id', 'username', 'email', 'posts']


class UserRestrictedSerializer(UserDetailsSerializer):
    """User serializer for user deteail."""

    class Meta:
        """Meta class for the serializer."""

        model = User
        fields = ['id', 'username', 'email', 'posts']
        read_only_fields = ('email', 'posts')
