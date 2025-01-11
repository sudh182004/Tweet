from django import forms
from .models import Tweet,Comments

class tweet_form(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']

