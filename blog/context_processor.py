from .models import Post, Category
from taggit.models import Tag

def menu_categories(request):
    categories = Category.objects.all()

    return {'menu_categories': categories}

def popular_posts(request):
    popular_posts = Post.objects.all().order_by('-num_visits')[0:6]
    # print(popular_posts)

    return {'popular_posts': popular_posts}

def tag_list(request):
    tags = Tag.objects.all()

    return {'tag_list': tags}

