from django.test import TestCase
from django.urls import resolve

from core.views import frontpage
from blog.views import category, tags

# Create your tests here.
#
# class TagTest(TestCase):

    # def test_root_url_resolves_to_tags_view(self):
    #     found = resolve('/tag/django/')
    #     self.assertEqual(found.func, tags)

class CetegoryTest(TestCase):

    def test_root_url_resolves_to_category_view(self):
        found = resolve('/django/')
        self.assertEqual(found.func, category)

    def test_uses_category_template(self):
        response = self.client.get('/django/')
        self.assertTemplateUsed(response, 'blog/category.html')