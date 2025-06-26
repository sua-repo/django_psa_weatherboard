from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from config import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("game/", include("game.urls")),  # dev_3 : game 앱 연결
    path("board/", include("board.urls")),  # dev_6 : board 앱 연결
    path("accounts/", include("accounts.urls")),  # dev_14 : accounts 앱 연결
    path("", include("main.urls")),  # dev_2 : 메인 페이지를 기본 경로로 연결
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
