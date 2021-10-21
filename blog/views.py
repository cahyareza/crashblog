from django.shortcuts import render, get_object_or_404, redirect

from .models import Post, Category

import random

from .forms import CommentForm

from django.db.models import Q


def detail(request, category_slug, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)

    related_posts = list(post.category.posts.filter(parent=None).exclude(id=post.id))
    if len(related_posts) >=3:
        related_posts = random.sample(related_posts, 3)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()

    return render(request, 'blog/detail.html', {'post': post, 'form': form, 'related_posts': related_posts })

def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status=Post.ACTIVE)


    return render(request, 'blog/category.html', {'category': category, 'posts':posts})

def search(request):
    query = request.GET.get('query', '')

    posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(intro__icontains=query) | Q(body__icontains=query))

    return render(request, 'blog/search.html', {'posts': posts, 'query': query})