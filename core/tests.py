from django.test import TestCase
from django.urls import resolve
from core.views import frontpage

# Create your tests here.

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, frontpage)

    def test_uses_home_template(self):
        response = self.client.get('/')
