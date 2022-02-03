from django.urls import path

from .views import detail, category, search, tags

urlpatterns = [
    path('search/', search, name='search'),
    path('<slug:category_slug>/<slug:slug>/', detail, name='post_detail'),
    path('<slug:slug>/', category, name='category_detail'),
    path('tag/<slug:tag_slug>/', tags, name='tag_list'),
]