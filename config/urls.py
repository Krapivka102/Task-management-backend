from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Перенаправление с корня на документацию API
    path('', RedirectView.as_view(url='/api/docs/')),
    # API маршруты
    path('api/v1/', include('apps.core.urls', namespace='core')),
    # Админка
    path('admin/', admin.site.urls),
    # Схема и документация API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
