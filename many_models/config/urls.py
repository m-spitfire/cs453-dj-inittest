from django.urls import path

from employees import views as employee_views
from manufacture import views as manufacture_views

urlpatterns = [
    path("countries/", employee_views.CountryList.as_view()),
    path("countries/<int:pk>/", employee_views.CountryDetail.as_view()),
    path("cities/", employee_views.CityList.as_view()),
    path("cities/<int:pk>/", employee_views.CityDetail.as_view()),
    path("companies/", employee_views.CompanyList.as_view()),
    path("companies/<int:pk>/", employee_views.CompanyDetail.as_view()),
    path("employees/", employee_views.EmployeeList.as_view()),
    path("employees/<int:pk>/", employee_views.EmployeeDetail.as_view()),
    path("manufacturers/", manufacture_views.ManufacturerList.as_view()),
    path("manufacturers/<int:pk>/", manufacture_views.ManufacturerDetail.as_view()),
    path("categories/", manufacture_views.CategoryList.as_view()),
    path("categories/<int:pk>/", manufacture_views.CategoryDetail.as_view()),
    path("products/", manufacture_views.ProductList.as_view()),
    path("products/<int:pk>/", manufacture_views.ProductDetail.as_view()),
    path("customers/", manufacture_views.CustomerList.as_view()),
    path("customers/<int:pk>/", manufacture_views.CustomerDetail.as_view()),
    path("reviews/", manufacture_views.ReviewList.as_view()),
    path("reviews/<int:pk>/", manufacture_views.ReviewDetail.as_view()),
    path("shippingaddresses/", manufacture_views.ShippingAddressList.as_view()),
    path(
        "shippingaddresses/<int:pk>/", manufacture_views.ShippingAddressDetail.as_view()
    ),
]
