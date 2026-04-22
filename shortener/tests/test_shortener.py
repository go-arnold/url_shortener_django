"""Tests for shortener domain logic and redirect behavior."""

import re

from django.test import TestCase

from shortener.models import ShortURL
from shortener.services.random_code_generator import RandomShortCodeGenerator


class RandomShortCodeGeneratorTests(TestCase):
    """Validate short code generation service."""

    def test_generate_returns_six_alphanumeric_characters(self):
        generator = RandomShortCodeGenerator()

        code = generator.generate()

        self.assertEqual(len(code), 6)
        self.assertRegex(code, re.compile(r"^[a-zA-Z0-9]{6}$"))


class RedirectShortURLTests(TestCase):
    """Validate short code redirect endpoint."""

    def test_redirects_existing_short_code(self):
        short_url = ShortURL.objects.create(
            original_url="https://example.com/resource",
            short_code="Ab12Cd",
        )

        response = self.client.get(f"/{short_url.short_code}/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, short_url.original_url)

    def test_redirect_returns_404_for_unknown_short_code(self):
        response = self.client.get("/ZZZZZZ/")

        self.assertEqual(response.status_code, 404)
