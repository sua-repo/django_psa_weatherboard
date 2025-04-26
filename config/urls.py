from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),  # dev_2 : 메인 페이지를 기본 경로로 연결
    path("game/", include("game.urls")),  # dev_3 : game 앱 연결
    path("board/", include("board.urls")),  # dev_6 : board 앱 연결
]
