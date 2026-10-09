from django.http import Http404, HttpRequest, HttpResponseRedirect
from django.urls import reverse
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shortener.serializers import (
    ExpandRequestSerializer,
    ExpandResponseSerializer,
    ShortenRequestSerializer,
    ShortenResponseSerializer,
)
from shortener.services import (
    CodeGenerationError,
    InvalidShortURLError,
    ShortURLNotFoundError,
    create_short_url,
    expand_short_url,
    get_original_url,
)


def build_short_url(request: HttpRequest, code: str) -> str:
    return request.build_absolute_uri(reverse("redirect", kwargs={"code": code}))


class ShortenView(APIView):
    def post(self, request: Request) -> Response:
        serializer = ShortenRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            link = create_short_url(serializer.validated_data["url"])
        except CodeGenerationError:
            return Response(
                {"detail": "Could not generate a unique code."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        payload = {
            "code": link.code,
            "short_url": build_short_url(request, link.code),
            "url": link.url,
        }
        return Response(
            ShortenResponseSerializer(payload).data,
            status=status.HTTP_201_CREATED,
        )


class ExpandView(APIView):
    def post(self, request: Request) -> Response:
        serializer = ExpandRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            url = expand_short_url(serializer.validated_data["short_url"])
        except InvalidShortURLError:
            return Response(
                {"short_url": ["Enter a valid short URL."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ShortURLNotFoundError:
            return Response(
                {"detail": "Not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(ExpandResponseSerializer({"url": url}).data)


def redirect_to_original(request: HttpRequest, code: str) -> HttpResponseRedirect:
    try:
        url = get_original_url(code)
    except ShortURLNotFoundError:
        raise Http404 from None
    return HttpResponseRedirect(url)
