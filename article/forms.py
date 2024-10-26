# forms.py
from django import forms
from .models import Comment  # Ensure Comment model is defined in your models.py


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # Adjust fields according to your Comment model
        fields = ['author_name', 'content']
