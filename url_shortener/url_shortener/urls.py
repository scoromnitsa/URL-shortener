from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view as yasg_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = yasg_schema_view(
    openapi.Info(
        title="URL Shortener API",
        default_version='v1',
        description="API for shortening URLs and tracking statistics",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shortener.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("docs/", schema_view.with_ui("swagger", cache_timeout=0), name='docs'),
]
