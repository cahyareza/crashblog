from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from blog.models import Post


def robots_txt(request):
    text = [
        "User-Agent: *",
        "Disallow: /admin/",
    ]

    return HttpResponse("\n".join(text), content_type="text/plain")

def frontpage(request):
    posts = Post.objects.filter(status=Post.ACTIVE)
    popular_posts = Post.objects.all().order_by('-num_visits')[0:4]
    paginator = Paginator(posts, 3)  # 3 posts in each page
    page = request.GET.get('page', 1)
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'page': page,
        'post_list': post_list,
        'popular_posts': popular_posts
    }

    return render(request, 'core/frontpage.html', context )

def about(request):
    return render(request, 'core/about.html')