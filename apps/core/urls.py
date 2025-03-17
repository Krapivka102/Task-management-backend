from django.urls import path
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter

from apps.core import views

router = DefaultRouter()

app_name = 'core'

urlpatterns = [
    path('', RedirectView.as_view(url='/api/docs/')),
    path('auth/', views.Auth.as_view(), name='auth'),
    path('logout/', views.Logout.as_view(), name='logout'),
]

router.register('projects', views.ProjectViewSet, basename='projects')

urlpatterns += router.urls
