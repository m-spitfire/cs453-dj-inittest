from comments.views import CommentList
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('comments/', CommentList.as_view())
]
