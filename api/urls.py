"""URL routes for API app."""

from django.urls import path

from api.views import ShortURLCreateAPIView

urlpatterns = [
    path("urls/", ShortURLCreateAPIView.as_view(), name="create-short-url"),
]
