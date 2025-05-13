from django.shortcuts import render
from .models import BlogContent

def blog_home(request):
    blog_contents = BlogContent.objects.all().order_by('-created_at')
    context = {
        'blog_contents': blog_contents,
    }
    return render(request, 'blog/blog_home.html', context)