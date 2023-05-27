from django import forms
from .models import Post,Comment

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta :
        model = Comment
        exclude = ["post"]
        labels = {
            "username":"Your name",
            "email_address":"Your email",
            "text":"Your comment"
        }