from django.contrib import admin
from django.urls import path, include

from rest_framework.permissions import AllowAny

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="metsenat API",
        default_version="v1",
        description="metsenat API description",
        terms_of_service="google.com",
        contact=openapi.Contact(email="example@gmail.com"),
        license=openapi.License(name="fake license")
    ),
    public=True,
    permission_classes=[AllowAny, ]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    
    #   swagger
    path('swagger/', schema_view.with_ui(
        'swagger', cache_timeout=0
    ), name='swagger-ui'),
    
    path('redoc/', schema_view.with_ui(
        'redoc', cache_timeout=0
    ), name='schema-redoc')
]
