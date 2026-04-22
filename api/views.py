"""API views for URL shortening workflows."""

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import CreateShortURLSerializer, ShortURLResponseSerializer


class ShortURLCreateAPIView(APIView):
    """Create short URLs from incoming long URLs."""

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
        short_url = serializer.save()

        response_serializer = ShortURLResponseSerializer(short_url)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
