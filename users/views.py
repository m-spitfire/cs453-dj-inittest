from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import generics, mixins, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer

User = get_user_model()


class UserList(APIView):
    def get(self, request: Request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request: Request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    def get_object(self, pk: int):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request: Request, pk: int, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request: Request, pk: int, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserFollow(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request: Request, pk: int, format=None):
        print("[LOG]")
        print(request.__dict__)
        # Cannot follow oneself
        if request.user.pk == pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # Already following the user
        if request.user.following.filter(pk=pk).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = self.get_object(pk)
        request.user.following.add(user)
        request.user.save()

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request: Request, pk: int, format=None):
        # Cannot follow oneself
        if request.user.pk == pk:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # Not following the user
        if not request.user.following.filter(pk=pk).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = self.get_object(pk)
        request.user.following.remove(user)
        request.user.save()

        return Response(status=status.HTTP_200_OK)
