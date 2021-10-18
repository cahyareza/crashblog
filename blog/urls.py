from django.urls import path

from .views import detail, category

urlpatterns = [
    path('<slug:category_slug>/<slug:slug>/', detail, name='post_detail'),
    path('<slug:slug>/', category, name='category_detail'),
]