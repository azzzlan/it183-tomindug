# Suggested code may be subject to a license. Learn more: ~LicenseLog:1050618240.
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')
