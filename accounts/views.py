from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
