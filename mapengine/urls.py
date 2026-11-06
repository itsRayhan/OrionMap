from django.urls import path
from .views import route_api, map_page

urlpatterns = [
    path("", map_page, name="map_page"),
    path("api/route/", route_api, name="route_api"),
]