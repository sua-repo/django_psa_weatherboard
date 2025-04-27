from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_user, name="login_user"),  # dev_15 : 로그인
    path("logout/", views.logout_user, name="logout_user"),  # dev_15 : 로그아웃
    path("signup/", views.signup_user, name="signup_user"),  # dev_16 : 회원가입
]
