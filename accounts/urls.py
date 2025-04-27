from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_user, name="login_user"),  # dev_15 : 로그인
    path("logout/", views.logout_user, name="logout_user"),  # dev_15 : 로그아웃
    path("signup/", views.signup_user, name="signup_user"),  # dev_16 : 회원가입
    path("mypage/", views.mypage, name="mypage"),  # dev_17 : 마이페이지
    path("edit/", views.edit_user, name="edit_user"),  # dev_17 : 마이페이지 정보 수정
]
