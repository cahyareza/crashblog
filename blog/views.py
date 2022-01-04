import random
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from .forms import CommentForm
from django.db.models import Q
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def detail(request, category_slug, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)
    post.num_visits = post.num_visits + 1
    post.last_visit = datetime.now()
    post.save()

    popular_posts = Post.objects.all().order_by('-num_visits')[0:4]
    related_posts = list(post.category.posts.filter(parent=None).exclude(id=post.id))
    if len(related_posts) >=4:
        related_posts = random.sample(related_posts, 4)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()

    return render(request, 'blog/detail.html', {'post': post, 'form': form, 'related_posts': related_posts, 'popular_posts': popular_posts})

def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status=Post.ACTIVE)
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
        'category': category,
        'posts':posts,
        'popular_posts': popular_posts,
        'post_list': post_list,
    }

    return render(request, 'blog/category.html', context)

def search(request):
    query = request.GET.get('query', '')

    posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(intro__icontains=query) | Q(body__icontains=query))

    return render(request, 'blog/search.html', {'posts': posts, 'query': query})