from django.urls import path
from . import views

app_name = "board"

urlpatterns = [
    path("", views.post_list, name="post_list"),  # dev_6 : 게시글 목록
    path("create/", views.post_create, name="post_create"),  # dev_8 : 게시글 작성
]
