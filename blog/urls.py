from django.urls import path

from .views import detail, category, search, tag

urlpatterns = [
    path('search/', search, name='search'),
    path('tag/<slug:tag_slug>/', tag, name='tag_list'),
    path('<slug:category_slug>/<slug:slug>/', detail, name='post_detail'),
    path('<slug:slug>/', category, name='category_detail'),
]