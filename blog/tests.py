from django.test import TestCase
from django.urls import resolve, reverse
from django.shortcuts import get_object_or_404

from core.views import frontpage
from blog.views import category, tag
from blog.models import Category, Post
from taggit.models import Tag
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your tests here.


class CategoryTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(title='Django', slug='django')

    def test_root_url_resolves_to_category_view(self):
        found = resolve(self.category.get_absolute_url())
        self.assertEqual(found.func, category)

    def test_uses_category_template(self):
        response = self.client.get(self.category.get_absolute_url())
        self.assertTemplateUsed(response, 'blog/category.html')

class TagTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='admin', email='jacob@…', password='top_secret')
        self.category = Category.objects.create(title='Django', slug='django')
        self.post = Post.objects.create(category=self.category, title='Example of tags',
            body='apa saja boleh asal jangan kosong', author=self.user, tags=['Django'])

        object_list = Post.objects.filter(status=Post.ACTIVE)
        tag = get_object_or_404(Tag, slug='django')
        object_list = object_list.filter(tags__in=[tag])

        paginator = Paginator(object_list, 10)  # 3 posts in each page
        page = request.GET.get('page', 1)
        try:
            self.post_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            self.post_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range deliver last page of results
            self.post_list = paginator.page(paginator.num_pages)


    def test_root_url_resolves_to_tags_view(self):
        found = resolve('/tag/django/')
        # print(found.url_name)

        self.assertEqual(found.func, tag)

    def test_uses_tag_template(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertTemplateUsed(response, 'blog/tags.html')