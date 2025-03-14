from django.views.generic import RedirectView
from django.urls import path

from apps.core import views


app_name = "core"

urlpatterns = [
    path("", RedirectView.as_view(url="/api/docs/")),
    path("auth/", views.Auth.as_view(), name="auth"),
]
