from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from .forms import PostForm
# Create your views here.
# Suggested code may be subject to a license. Learn more: ~LicenseLog:1661712556.
from django.shortcuts import render
from .models import Post

# Suggested code may be subject to a license. Learn more: ~LicenseLog:3215286551.
from django import forms
from .models import Post


def index(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the index page after creating a post
    else:
        form = PostForm()

    context = {'posts': posts, 'form': form}
    return render(request, 'index.html', context)

# Suggested code may be subject to a license. Learn more: ~LicenseLog:3728279174.
# Suggested code may be subject to a license. Learn more: ~LicenseLog:2370036352.

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('index')  # Redirect to the index page after deletion
    context = {'post': post}
    return render(request, 'post_detail.html', context)

# Suggested code may be subject to a license. Learn more: ~LicenseLog:2224225373.
# Suggested code may be subject to a license. Learn more: ~LicenseLog:1840908862.
# Suggested code may be subject to a license. Learn more: ~LicenseLog:51608532.
# Suggested code may be subject to a license. Learn more: ~LicenseLog:1035085478.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form, 'post': post})
