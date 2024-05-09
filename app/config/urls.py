from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from rest_framework.routers import DefaultRouter
from rest_framework import authentication, permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from app.hotels.views import HotelViewSet, HotelChainViewSet, HotelDraftViewSet

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

admin.site.site_header = "Hotel API"
admin.site.site_title = "Hotel API"
admin.site.index_title = "Welcome to Hotel API"

schema_view = get_schema_view(
    openapi.Info(
        title="Hotel API",
        default_version="v1",
        description="Welcome to the Documentation of Hotel API",
    ),
    public=True,
    authentication_classes=(authentication.BasicAuthentication,),
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r"hotels", HotelViewSet)
router.register(r"hotelchains", HotelChainViewSet)
router.register(r"hoteldrafts", HotelDraftViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "api/v1/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/v1/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("api/v1/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
