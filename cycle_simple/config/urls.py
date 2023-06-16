from django.contrib import admin
from django.urls import path

from comments.views import CommentList


urlpatterns = [
    path('admin/', admin.site.urls),
    path('comments/', CommentList.as_view())
]
