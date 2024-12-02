from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm

def index(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the index page after creating a post
    else:
        form = PostForm()

    context = {'posts': posts, 'form': form}
    return render(request, 'index.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':  # Handle delete request
        post.delete()
        return redirect('index')  # Redirect to the index page after deletion
    context = {'post': post}
    return render(request, 'post_detail.html', context)

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)  # Include request.FILES for file uploads
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the index page after saving
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})

def rate_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        rating = int(request.POST.get("rating", 0))
        if 1 <= rating <= 5:  # Ensure valid rating
            post.rating = rating
            post.save()
    return redirect('index')  # Redirect back to the homepage

def top_rated_posts(request):
    # Order posts by rating in descending order (highest first)
    posts = Post.objects.all().order_by('-rating')
    return render(request, 'top_rated.html', {'posts': posts})
