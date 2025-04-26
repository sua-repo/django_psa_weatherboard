from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from .models import Image, Post
from datetime import date
from django.contrib.auth.decorators import login_required


# Create your views here.
# dev_6
def post_list(request):
    posts = Post.objects.order_by("-created_at")  # 최신순 정렬
    paginator = Paginator(posts, 10)  # 한 페이지에 10개씩 보여주는 페이지네이터 생성
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(
        page_number
    )  # 현재 페이지 번호에 해당하는 게시글 리스트 추출

    context = {
        "posts": page_obj,
        "today": date.today(),
    }
    return render(request, "board/post_list.html", context)


# dev_8
@login_required
def post_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category = request.POST.get("category")
        images = request.FILES.getlist('images')  # 여러 개 이미지 파일 가져오기

        # 먼저 글(Post) 저장
        post = Post.objects.create(
            author=request.user,
            title=title,
            content=content,
            category=category,
        )

        # 그 Post에 연결해서 이미지들도 저장
        for img in images:
            Image.objects.create(
                post=post,
                image=img
            )
        return redirect("board:post_list")  # 작성 후 글 목록으로 이동

    return render(request, "board/post_create.html")
