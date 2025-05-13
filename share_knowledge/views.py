from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Post, Comment
from .forms import PostForm, CommentForm
import random

@login_required
def feed(request):
    posts = list(Post.objects.all().order_by('-created_at'))
    random.shuffle(posts)
    form = PostForm()
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'form': form,
        'comment_form': comment_form,
    }
    return render(request, 'share_knowledge/feed.html', context)

@login_required
@require_POST
def create_post(request):
    form = PostForm(request.POST, request.FILES)  # รับ FILES ด้วย
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
    return redirect('share_knowledge:feed')

@login_required
@require_POST
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
    return redirect('share_knowledge:feed')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('share_knowledge:feed')

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user:
        post.delete()
    return redirect('share_knowledge:feed')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:
        comment.delete()
    return redirect('share_knowledge:feed')