from django.contrib import admin
from django.urls import path

import posts
from posts import views as post_views
from employees import views as employee_views
from users.views import UserDetail, UserList


urlpatterns = [
    path("admin/", admin.site.urls),
    path("posts/", posts.views.PostList.as_view()),
    path("posts/<int:pk>/", post_views.PostDetail.as_view()),
    path("comments/", post_views.CommentList.as_view()),
    path("comments/<int:pk>/", post_views.CommentDetail.as_view()),
    path("countries/", employee_views.CountryList.as_view()),
    path("countries/<int:pk>/", employee_views.CountryDetail.as_view()),
    path("cities/", employee_views.CityList.as_view()),
    path("cities/<int:pk>/", employee_views.CityDetail.as_view()),
    path("companies/", employee_views.CompanyList.as_view()),
    path("companies/<int:pk>/", employee_views.CompanyDetail.as_view()),
    path("employees/", employee_views.EmployeeList.as_view()),
    path("employees/<int:pk>/", employee_views.EmployeeDetail.as_view()),
    path("users/", UserList.as_view()),
    path("users/<int:pk>/", UserDetail.as_view()),
]
