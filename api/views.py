"""API views for URL shortening workflows."""

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import CreateShortURLSerializer, ShortURLResponseSerializer
from shortener.models import ShortURL
from shortener.services.random_code_generator import RandomShortCodeGenerator


class ShortURLCreateAPIView(APIView):
    """Create short URLs from incoming long URLs."""

    code_generator = RandomShortCodeGenerator()

    @extend_schema(
        request=CreateShortURLSerializer,
        responses={201: ShortURLResponseSerializer},
    )
    def post(self, request):
        """Create a short URL resource.

        Args:
            request: Request containing `original_url`.

        Returns:
            Response: Serialized short URL data.
        """
        serializer = CreateShortURLSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        original_url = serializer.validated_data["original_url"]
        short_url = ShortURL.objects.filter(original_url=original_url).first()
        if short_url is None:
            short_code = self._generate_unique_short_code()
            short_url = ShortURL.objects.create(original_url=original_url, short_code=short_code)

        response_serializer = ShortURLResponseSerializer(short_url)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def _generate_unique_short_code(self) -> str:
        """Generate short codes until a unique value is found.

        Returns:
            str: A unique 6-character short code.
        """
        while True:
            candidate = self.code_generator.generate(length=6)
            if not ShortURL.objects.filter(short_code=candidate).exists():
                return candidate
