from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from .models import Comment, Image, Post
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
# dev_6 : 게시글 목록
# dev_9 : 카테고리 필터링
def post_list(request):
    category = request.GET.get("category")  # '일반' / '코디' / None
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


# dev_8 : 게시글 작성
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


# dev_9 : 게시글 상세보기
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    images = post.images.all()  # 해당 게시글에 연결된 이미지들

    context = {"post": post, "images": images}

    return render(request, "board/post_detail.html", context)


# dev_10 : 게시글 수정
@login_required
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # 작성자만 수정 가능
    if request.user != post.author:
        return redirect("board:post_list")

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category = request.POST.get("category")
        delete_images = request.POST.get("delete_images")  # 삭제할 이미지 id들
        images = request.FILES.getlist("images")

        post.title = title
        post.content = content
        post.category = category
        post.save()

        # 이미지 삭제
        # 기존 이미지 삭제 처리
        if delete_images:
            delete_ids = delete_images.split(",")
            from .models import Image

            Image.objects.filter(id__in=delete_ids).delete()

        # 새로 추가된 이미지 저장
        for img in images:
            Image.objects.create(post=post, image=img)

        return redirect("board:post_detail", post_id=post.id)

    context = {
        "post": post,
        "images": post.images.all(),  # 기존 이미지들 넘겨주기
    }

    return render(request, "board/post_update.html", context)


# dev_10 : 게시글 삭제
@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # 작성자만 삭제 가능
    if request.user == post.author:
        post.delete()

    return redirect("board:post_list")  # 삭제 후 글 목록으로 이동


# dev_11 : 댓글 작성
@login_required
def comment_create(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        content = request.POST.get("content")
        image = request.FILES.get("image")

        # 이미지와 내용 둘 다 없을 땐 작성 막기
        # if not content and not image:
        #    return redirect("board:post_detail", post_id=post.id)

        # 이미지나 내용 중 하나라도 있으면 댓글 작성
        if content or image:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content,
                image=image,
            )
            return redirect("board:post_detail", post_id=post.id)

        else:
            messages.error(
                request, "내용이나 이미지를 입력해야 댓글을 작성할 수 있습니다."
            )
            return redirect("board:post_detail", post_id=post.id)

    comments = Comment.objects.filter(post=post).order_by("created_at")
    return redirect("board:post_detail", post_id=post.id)


# dev_12 : 댓글 수정
@login_required
def comment_update(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # 작성자만 수정 가능
    if request.user != comment.author:
        messages.error(request, "수정 권한이 없습니다.")
        return redirect("board:post_detail", post_id=comment.post.id)

    if request.method == "POST":
        content = request.POST.get("content")
        image = request.POST.get("image")

        # 내용과 이미지 중 하나라도 있으면 수정 가능
        if content or image:
            comment.content = content
            if image:
                comment.image = image  # 새 이미지 등록하면 바꿔줌
            comment.save()

            messages.success(request, "댓글이 수정되었습니다.")
            return redirect("board:post_detail", post_id=comment.post.id)

        else:
            messages.error(request, "내용이나 이미지를 입력해야 합니다.")
            return redirect("board:post_detail", post_id=comment.post.id)

    return render(request, "board/comment_update.html", {"comment": comment})


# dev_12 : 댓글 삭제
@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # 작성자만 삭제 가능
    if request.user != comment.author:
        messages.error(request, "삭제 권한이 없습니다.")
        return redirect("board:post_detail", post_id=comment.post.id)

    comment.delete()
    messages.success(request, "댓글이 삭제되었습니다.")
    return redirect("board:post_detail", post_id=comment.post.id)


# dev_13 : 추천 기능
@login_required
def post_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # 추천한 상태에서 한 번 더 누르면 추천 취소
    if request.user in post.likes.all():
        post.likes.remove(request.user)

    else:
        post.likes.add(request.user)

    return redirect("board:post_detail", post_id=post.id)


# dev_13 : 스크랩 기능
@login_required
def post_scrap(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # 스크랩한 상태에서 한 번 더 누르면 스크랩 취소
    if request.user in post.scraps.all():
        post.scraps.remove(request.user)

    else:
        post.scraps.add(request.user)

    return redirect("board:post_detail", post_id=post.id)
