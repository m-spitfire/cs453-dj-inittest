from django.contrib import admin
from django.urls import path

from publications.views import PublicationList, PublicationDetail, ArticleList, ArticleDetail


urlpatterns = [
    path('admin/', admin.site.urls),
    path('publications/', PublicationList.as_view()),
    path('publications/<int:pk>/', PublicationDetail.as_view()),
    path('articles/', ArticleList.as_view()),
    path('articles/<int:pk>/', ArticleDetail.as_view()),
]
