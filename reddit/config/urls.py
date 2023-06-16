from django.contrib import admin
from django.urls import path


from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', core_views.UserList.as_view()),
    path('users/<int:pk>/', core_views.UserDetail.as_view()),
    path('m2musers/', core_views.M2mUserList.as_view()),
    path('m2musers/<int:pk>/', core_views.M2mUserDetail.as_view()),
    path('subs/', core_views.SubredditList.as_view()),
    path('subs/<int:pk>/', core_views.SubredditDetail.as_view()),
    path('posts/', core_views.PostList.as_view()),
    path('posts/<int:pk>/', core_views.PostDetail.as_view()),
    path('comments/', core_views.CommentList.as_view()),
    path('comments/<int:pk>/', core_views.CommentDetail.as_view()),
]
