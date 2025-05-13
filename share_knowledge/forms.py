from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'แบ่งปันความรู้ของคุณ...'}))
    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['content', 'image']

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'แสดงความคิดเห็น...'}))

    class Meta:
        model = Comment
        fields = ['content']