from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', RedirectView.as_view(url='/backend/')),
    path('backend/', include('core.urls', namespace='core')),
    path('backend/admin/', admin.site.urls),
    path('backend/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('backend/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('backend/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]

if settings.DEBUG:
    urlpatterns += static('media', document_root=settings.MEDIA_ROOT)