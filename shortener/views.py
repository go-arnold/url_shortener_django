"""Views for short URL redirect behavior."""

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from drf_spectacular.openapi import OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework.views import APIView

from shortener.models import ShortURL


class RedirectShortURLView(APIView):
    """View for redirecting short codes to their original URLs."""

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="short_code",
                location=OpenApiParameter.PATH,
                description="6-character short URL code",
                required=True,
                type=OpenApiTypes.STR,
            ),
        ],
        responses={
            302: None,  # Redirect response
            404: OpenApiResponse(description="Short code not found"),
        },
        description="Redirect a short code to its original URL.",
        summary="Redirect short URL",
    )
    def get(self, request, short_code: str) -> HttpResponseRedirect:
        """Redirect a short code request to its original URL.

        Args:
            request: Incoming HTTP request.
            short_code: Short URL code to resolve (6 characters).

        Returns:
            HttpResponseRedirect: HTTP 302 redirect to original URL.

        Raises:
            Http404: If the short code is invalid or unknown.
        """
        if not short_code or len(short_code) != 6:
            raise Http404("Short code not found.")
        short_url = get_object_or_404(ShortURL, short_code=short_code)
        return HttpResponseRedirect(short_url.original_url)
