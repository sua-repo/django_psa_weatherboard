from django.contrib import admin
from django.urls import include, path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),  # dev_2 : 홈화면
    path(
        "get-address/", views.get_address, name="get_address"
    ),  # dev_5 : 주소 검색 api
    path(
        "get-weather/", views.get_weather, name="get_weather"
    ),  # dev_20 : 날씨 가져오기
]
