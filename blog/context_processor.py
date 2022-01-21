from .models import Post, Category

def menu_categories(request):
    categories = Category.objects.all()

    return {'menu_categories': categories}

def popular_posts(request):
    popular_posts = Post.objects.all().order_by('-num_visits')[0:4]

    return {'popular_posts': popular_posts}

