from dj_rest_auth.registration.views import VerifyEmailView
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from posts import views as post_views
from users import views as user_views

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.register("users", user_views.UserViewSet)
router.register("posts", post_views.PostViewSet)
router.register("auth/user/posts", post_views.UserPostsViewSet, basename="user-posts")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path(
            'api/schema/swagger-ui/',
            SpectacularSwaggerView.as_view(url_name='schema'),
            name='swagger-ui'
        ),
    ]
