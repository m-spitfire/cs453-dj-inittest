from django.contrib import admin
from django.urls import path

from posts import views as post_views
from users import views as user_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', post_views.PostList.as_view()),
    path('posts/<int:pk>/', post_views.PostDetail.as_view()),
    path('comments/', post_views.CommentList.as_view()),
    path('comments/<int:pk>/', post_views.CommentList.as_view()),
    path('users/', user_views.UserList.as_view()),
    path('users/<int:pk>/', user_views.UserDetail.as_view()),
]
