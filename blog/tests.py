from django.test import TestCase
from blog.forms import CommentForm

# Create your tests here.

class CommentFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        form = CommentForm()
        self.fail(form.as_p())
