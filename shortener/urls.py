from django.urls import path

from shortener.views import ExpandView, ShortenView

urlpatterns = [
    path("shorten/", ShortenView.as_view(), name="shorten"),
    path("expand/", ExpandView.as_view(), name="expand"),
]
