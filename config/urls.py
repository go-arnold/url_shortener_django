"""Main URL routing for the URL shortener project."""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from shortener.views import RedirectShortURLView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/", include("api.urls")),
    path("<str:short_code>/", RedirectShortURLView.as_view(), name="redirect-short-url"),
]
