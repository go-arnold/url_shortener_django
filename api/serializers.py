"""Serializer definitions for URL API."""

from rest_framework import status
from rest_framework import serializers
from rest_framework.exceptions import APIException

from shortener.models import ShortURL
from shortener.services.random_code_generator import RandomShortCodeGenerator


class ShortCodeGenerationError(APIException):
    """Raised when a unique short code cannot be generated."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Unable to generate a short code at the moment. Please retry."
    default_code = "short_code_generation_unavailable"


class CreateShortURLSerializer(serializers.ModelSerializer):
    """Serializer for creating short URLs with strict URL validation."""

    code_generator = RandomShortCodeGenerator()
    max_generation_attempts = 20

    class Meta:
        model = ShortURL
        fields = ["original_url"]

    def create(self, validated_data):
        """Create or reuse a short URL for a validated original URL."""
        original_url = validated_data["original_url"]

        existing_short_url = ShortURL.objects.filter(original_url=original_url).first()
        if existing_short_url is not None:
            return existing_short_url

        short_code = self._generate_unique_short_code()
        return ShortURL.objects.create(original_url=original_url, short_code=short_code)

    def _generate_unique_short_code(self) -> str:
        """Generate short codes until a unique value is found."""
        for _ in range(self.max_generation_attempts):
            candidate = self.code_generator.generate(length=6)
            if not ShortURL.objects.filter(short_code=candidate).exists():
                return candidate
        raise ShortCodeGenerationError()


class ShortURLResponseSerializer(serializers.ModelSerializer):
    """Serializer for short URL API responses."""

    class Meta:
        model = ShortURL
        fields = ["short_code", "original_url"]
