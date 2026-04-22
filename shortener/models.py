"""Database models for URL shortening."""

from django.db import models


class ShortURL(models.Model):
    """Represents a stored original URL and its short code mapping."""

    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return readable short URL mapping description.

        Returns:
            str: Human-readable representation.
        """
        return f"{self.short_code} -> {self.original_url}"
