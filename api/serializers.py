"""Serializer definitions for URL API."""

from rest_framework import serializers

from shortener.models import ShortURL


class CreateShortURLSerializer(serializers.ModelSerializer):
    """Serializer for creating short URLs with strict URL validation."""

    class Meta:
        model = ShortURL
        fields = ["original_url"]


class ShortURLResponseSerializer(serializers.ModelSerializer):
    """Serializer for short URL API responses."""

    class Meta:
        model = ShortURL
        fields = ["short_code", "original_url"]
