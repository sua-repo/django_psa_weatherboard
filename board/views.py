from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Post
from datetime import date


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
