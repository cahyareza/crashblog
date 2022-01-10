import random
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
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

    # List of active comments for this post
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = form.save(commit=False)
            # reply-section
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            # Assign the current reply to the comment
            new_comment.reply = comment_qs
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()

            form = CommentForm()
    else:
        form = CommentForm()

    return render(request, 'blog/detail.html', {'post': post, 'form': form, 'related_posts': related_posts, 'popular_posts': popular_posts, 'comments': comments})

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
    popular_posts = Post.objects.all().order_by('-num_visits')[0:4]

    posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(intro__icontains=query) | Q(body__icontains=query))

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
        'posts':posts,
        'post_list': post_list,
        'popular_posts': popular_posts,
        'query': query
    }

    return render(request, 'blog/search.html', context)