from typing import Any
from urllib.parse import urlsplit

from rest_framework import serializers


class ShortenRequestSerializer(serializers.Serializer[Any]):
    url = serializers.URLField(max_length=2048)

    def validate_url(self, value: str) -> str:
        if urlsplit(value).scheme not in {"http", "https"}:
            raise serializers.ValidationError("Only http and https URLs are allowed.")
        return value


class ShortenResponseSerializer(serializers.Serializer[Any]):
    code = serializers.CharField()
    short_url = serializers.URLField()
    url = serializers.URLField()


class ExpandRequestSerializer(serializers.Serializer[Any]):
    short_url = serializers.URLField()


class ExpandResponseSerializer(serializers.Serializer[Any]):
    url = serializers.URLField()
