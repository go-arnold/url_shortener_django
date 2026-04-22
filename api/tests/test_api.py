"""Tests for URL creation API."""

from unittest import mock

from rest_framework import status
from rest_framework.test import APITestCase

from shortener.models import ShortURL


class ShortURLCreateAPITests(APITestCase):
    """Validate URL shortening API behavior."""

    def test_create_short_url_success(self):
        response = self.client.post("/api/urls/", {"original_url": "https://example.com/path"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data["short_code"]), 6)
        self.assertEqual(response.data["original_url"], "https://example.com/path")
        self.assertTrue(ShortURL.objects.filter(short_code=response.data["short_code"]).exists())

    def test_create_short_url_rejects_invalid_url(self):
        response = self.client.post("/api/urls/", {"original_url": "not-a-valid-url"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("original_url", response.data)

    @mock.patch("api.serializers.CreateShortURLSerializer.max_generation_attempts", 1)
    @mock.patch("api.serializers.RandomShortCodeGenerator.generate", return_value="Ab12Cd")
    def test_create_short_url_returns_503_when_unique_code_cannot_be_generated(self, _mock_generate):
        ShortURL.objects.create(original_url="https://example.com/existing", short_code="Ab12Cd")

        response = self.client.post("/api/urls/", {"original_url": "https://example.com/new"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)