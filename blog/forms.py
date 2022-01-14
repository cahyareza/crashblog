from django import forms

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        labels = {
            'body': 'Message',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'input',
                    'placeholder': 'Enter a name',
                    # 'oninvalid': "setCustomValidity('This field is required')",
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'input',
                    'placeholder': 'Email an email',
                    'value': "hello@",
                }),
            'body': forms.Textarea(
                attrs = {
                    'class': 'textarea',
                    'placeholder': 'Enter a comment',
                })

        }

        help_texts = {
            'email': 'Enter required email'
        }

