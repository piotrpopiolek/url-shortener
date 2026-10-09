from django.urls import include, path

from shortener.views import redirect_to_original

urlpatterns = [
    path("api/", include("shortener.urls")),
    path("shrt/<str:code>", redirect_to_original, name="redirect"),
]
