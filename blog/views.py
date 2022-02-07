import random
import pytz
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Comment
from .forms import CommentForm
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from taggit.models import Tag


def detail(request, category_slug, slug):

    # post

    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)
    post.num_visits = post.num_visits + 1
    post.last_visit = timezone.now()
    post.save()

    related_posts = list(post.category.posts.filter(parent=None).exclude(id=post.id))
    if len(related_posts) >=6:
        related_posts = random.sample(related_posts, 6)

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

    context = {
        'post': post,
        'form': form,
        'related_posts': related_posts,
        'comments': comments,
        'figcaption': post.image_footer,
    }

    return render(request, 'blog/detail.html', context)

def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status=Post.ACTIVE)

    paginator = Paginator(posts, 10)  # 3 posts in each page
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
        'post_list': post_list,
        'category_slug': slug
    }

    return render(request, 'blog/category.html', context)

def search(request):
    query = request.GET.get('query', '')

    posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(body__icontains=query))

    paginator = Paginator(posts, 10)  # 3 posts in each page
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
        'query': query
    }

    return render(request, 'blog/search.html', context)

def tag(request, tag_slug=None):
    object_list = Post.objects.filter(status=Post.ACTIVE)
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 10)  # 3 posts in each page
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
        'post_list': post_list,
        'tag': tag,
    }

    return render(request, 'blog/tags.html', context)
