from django import forms
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content' : forms.Textarea(attrs={'rows' : 2, 'placeholder' : 'What\'s happening today?'})
        }