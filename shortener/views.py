"""Views for short URL redirect behavior."""

from django.http import Http404, HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from shortener.models import ShortURL


def redirect_short_url(request: HttpRequest, short_code: str) -> HttpResponseRedirect:
    """Redirect a short code request to its original URL.

    Args:
        request: Incoming HTTP request.
        short_code: Short URL code to resolve.

    Returns:
        HttpResponseRedirect: HTTP 302 redirect to original URL.

    Raises:
        Http404: If the short code is unknown.
    """
    if not short_code or len(short_code) != 6:
        raise Http404("Short code not found.")
    short_url = get_object_or_404(ShortURL, short_code=short_code)
    return HttpResponseRedirect(short_url.original_url)
