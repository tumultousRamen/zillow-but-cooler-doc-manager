from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'documents', views.DocumentViewSet, basename='document')
router.register(r'properties', views.PropertyViewSet, basename='property')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]