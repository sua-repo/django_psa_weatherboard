from django.urls import path
from . import views

app_name = "board"

urlpatterns = [
    path("", views.post_list, name="post_list"),  # dev_6 : 게시글 목록
    path("create/", views.post_create, name="post_create"),  # dev_8 : 게시글 작성
    path(
        "<int:post_id>/", views.post_detail, name="post_detail"
    ),  # dev_9 : 게시글 작성
    path(
        "update/<int:post_id>/", views.post_update, name="post_update"
    ),  # dev_10 : 게시글 수정
    path(
        "delete/<int:post_id>/", views.post_delete, name="post_delete"
    ),  # dev_10 : 게시글 삭제
    path(
        "comment/<int:post_id>/", views.comment_create, name="comment_create"
    ),  # dev_11 : 댓글 작성
    path(
        "comment/update/<int:comment_id>/", views.comment_update, name="comment_update"
    ),  # dev_12 : 댓글 수정
    path(
        "comment/delete/<int:comment_id>/", views.comment_delete, name="comment_delete"
    ),  # dev_12 : 댓글 삭제
    path(
        "post/<int:post_id>/like/", views.post_like, name="post_like"
    ),  # dev_13 : 추천
    path(
        "post/<int:post_id>/scrap/", views.post_scrap, name="post_scrap"
    ),  # dev_13 : 스크랩
]
