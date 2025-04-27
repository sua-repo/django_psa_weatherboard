from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

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
@login_required
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


# dev_17 : 마이페이지
@login_required
def mypage(request):
    user = request.user

    filter_type = request.GET.get("filter", "all")
    page = request.GET.get("page")

    # 내가 쓴 글 (최신순 정렬)
    my_posts = user.post_set.all().order_by("-created_at")

    # 내가 쓴 댓글 (최신순 정렬)
    my_comments = user.comment_set.all().order_by("-created_at")

    # 내가 추천한 글 (최신순 정렬)
    liked_posts = user.liked_posts.all().order_by("-created_at")

    # 내가 스크랩한 글 (최신순 정렬)
    scrapped_posts = user.scrapped_posts.all().order_by("-created_at")

    # 필터별 데이터
    if filter_type == "posts":
        paginator = Paginator(my_posts, 10)
        items = paginator.get_page(page)
    elif filter_type == "comments":
        paginator = Paginator(my_comments, 10)
        items = paginator.get_page(page)
    elif filter_type == "likes":
        paginator = Paginator(liked_posts, 10)
        items = paginator.get_page(page)
    elif filter_type == "scraps":
        paginator = Paginator(scrapped_posts, 10)
        items = paginator.get_page(page)
    else:
        # 전체일 때만 5개씩 자름
        my_posts_preview = my_posts[:5]
        my_comments_preview = my_comments[:5]
        liked_posts_preview = liked_posts[:5]
        scrapped_posts_preview = scrapped_posts[:5]
        my_posts = my_posts  # 전체 데이터 그대로 유지
        my_comments = my_comments
        liked_posts = liked_posts
        scrapped_posts = scrapped_posts
        items = None

    context = {
        "filter_type": filter_type,
        "my_posts": my_posts_preview if filter_type == "all" else my_posts,
        "my_comments": my_comments_preview if filter_type == "all" else my_comments,
        "liked_posts": liked_posts_preview if filter_type == "all" else liked_posts,
        "scrapped_posts": (
            scrapped_posts_preview if filter_type == "all" else scrapped_posts
        ),
        "items": items,
    }
    return render(request, "accounts/mypage.html", context)


# dev_17 : 마이페이지 정보 수정
def edit_user(request):
    if request.method == "POST":
        cold_sensitivity = request.POST.get("cold_sensitivity")
        heat_sensitivity = request.POST.get("heat_sensitivity")

        profile = Profile.objects.get(user=request.user)
        profile.cold_sensitivity = cold_sensitivity
        profile.heat_sensitivity = heat_sensitivity
        profile.save()

        messages.success(request, "정보가 수정되었습니다.")
        return redirect("accounts:mypage")

    else:
        profile = Profile.objects.get(user=request.user)

        context = {
            "user": request.user,
            "profile": profile,
        }

        return render(request, "accounts/edit_user.html", context)
