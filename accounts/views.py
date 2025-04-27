from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Create your views here.


# dev_15 : 로그인
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "로그인 성공!")
            return redirect("main:index")  # 로그인 성공하면 홈화면

        else:
            messages.error(request, "아이디 또는 비밀번호가 틀렸습니다.")

    return render(request, "accounts/login.html")


# dev_15 : 로그아웃
def logout_user(request):
    logout(request)
    messages.success(request, "로그아웃되었습니다.")
    return redirect("main:index")  # 로그아웃 후 홈화면


# dev_16 : 회원가입
def signup_user(request):
    if request.method == "POST":
        # 회원가입 처리
        username = request.POST.get("username")
        password = request.POST.get("password")
        real_name = request.POST.get("real_name")
        birthdate = request.POST.get("birthdate")
        gender = request.POST.get("gender")
        cold_sensitivity = request.POST.get("cold_sensitivity")
        heat_sensitivity = request.POST.get("heat_sensitivity")

        # 아이디 중복 체크
        if User.objects.filter(username=username).exists():
            messages.error(request, "이미 존재하는 아이디입니다.")
            return redirect("accounts:signup_user")

        # User 모델엔 아이디, 비번, 이름만 저장
        user = User.objects.create(
            username=username, password=make_password(password), first_name=real_name
        )

        # 그 외엔 Profile 모델에 저장
        Profile.objects.create(
            user=user,
            birthdate=birthdate,
            gender=gender,
            cold_sensitivity=cold_sensitivity,
            heat_sensitivity=heat_sensitivity,
        )

        messages.success(request, "회원가입이 완료되었습니다!")
        return redirect("accounts:login_user")  # 회원가입 후 로그인 페이지로 이동

    return render(request, "accounts/signup.html")
