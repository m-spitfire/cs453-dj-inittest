from django.urls import path

from employees import views as employee_views


urlpatterns = [
    path("countries/", employee_views.CountryList.as_view()),
    path("countries/<int:pk>/", employee_views.CountryDetail.as_view()),
    path("cities/", employee_views.CityList.as_view()),
    path("cities/<int:pk>/", employee_views.CityDetail.as_view()),
    path("companies/", employee_views.CompanyList.as_view()),
    path("companies/<int:pk>/", employee_views.CompanyDetail.as_view()),
    path("employees/", employee_views.EmployeeList.as_view()),
    path("employees/<int:pk>/", employee_views.EmployeeDetail.as_view()),
]
