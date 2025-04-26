from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from .models import Image, Post
from datetime import date
from django.contrib.auth.decorators import login_required


# Create your views here.
# dev_6
# dev_9 : 카테고리 필터링
def post_list(request):
    category = request.GET.get('category')  # '일반' / '코디' / None
    posts = Post.objects.all()

    if category:  # 카테고리로 필터링
        posts = posts.filter(category=category)

    posts = posts.order_by("-created_at")

    paginator = Paginator(posts, 10)  # 한 페이지에 10개씩 보여주는 페이지네이터 생성
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(
        page_number
    )  # 현재 페이지 번호에 해당하는 게시글 리스트 추출

    context = {
        "posts": page_obj,
        "today": date.today(),
        "selected_category": category,
    }
    return render(request, "board/post_list.html", context)


# dev_8
@login_required
def post_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category = request.POST.get("category")
        images = request.FILES.getlist("images")  # 여러 개 이미지 파일 가져오기

        # 먼저 글(Post) 저장
        post = Post.objects.create(
            author=request.user,
            title=title,
            content=content,
            category=category,
        )

        # 그 Post에 연결해서 이미지들도 저장
        for img in images:
            Image.objects.create(post=post, image=img)
        return redirect("board:post_list")  # 작성 후 글 목록으로 이동

    return render(request, "board/post_create.html")


# dev_9
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    images = post.images.all()  # 해당 게시글에 연결된 이미지들

    context = {"post": post, "images": images}

    return render(request, "board/post_detail.html", context)
