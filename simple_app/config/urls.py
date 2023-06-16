from django.contrib import admin
from django.urls import path

import posts
from posts import views as post_views
from users.views import UserDetail, UserList

urlpatterns = [
    path("admin/", admin.site.urls),
    path("posts/", posts.views.PostList.as_view()),
    path("posts/<int:pk>/", post_views.PostDetail.as_view()),
    path("comments/", post_views.CommentList.as_view()),
    path("comments/<int:pk>/", post_views.CommentDetail.as_view()),
    path("users/", UserList.as_view()),
    path("users/<int:pk>/", UserDetail.as_view()),
]
