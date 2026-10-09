from django.db import models


class Link(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=16, unique=True)
    url = models.URLField(max_length=2048)

    def __str__(self) -> str:
        return f"{self.code} -> {self.url}"
