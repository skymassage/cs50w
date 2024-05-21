from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields= ["content"]

        widgets = {
            "content": forms.Textarea(attrs={"placeholder":"Your post", "rows":5, "class": "form-control"}),
        }