from django.urls import path

from .views import detail

urlpatterns = [
    path('<slug:slug>/', detail, name='post_detail'),
]