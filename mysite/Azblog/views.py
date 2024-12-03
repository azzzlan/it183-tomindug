from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, PostRating
from .forms import PostForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

@login_required
def index(request):
    posts = Post.objects.all()

    # Adding user-specific rating data
    for post in posts:
        user_rating = post.ratings.filter(user=request.user).first()
        post.user_rating = user_rating.value if user_rating else 0  # Store user's rating for each post

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            # Assign the logged-in user as the author of the post
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('index')  # Redirect to the index page after creating a post
    else:
        form = PostForm()

    context = {'posts': posts, 'form': form}
    return render(request, 'index.html', context)

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':  # Handle delete request
        if post.author != request.user:  # Ensure only the author can delete
            return HttpResponseForbidden("You are not allowed to delete this post.")
        else:
            post.delete()
            return redirect('index')  # Redirect to the index page after deletion
    context = {'post': post}
    return render(request, 'post_detail.html', context)

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:  # Ensure only the author can delete
        return HttpResponseForbidden("You are not allowed to delete this post.")
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)  # Include request.FILES for file uploads
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the index page after saving
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})

@login_required
def rate_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        rating = int(request.POST.get("rating", 0))
        if 1 <= rating <= 5:  # Ensure valid rating
            post_rating, created = PostRating.objects.update_or_create(
                user=request.user,
                post=post,
                defaults={'value': rating}
            )
    return redirect('index')  # Redirect back to the homepage


@login_required
def top_rated_posts(request):
    # Efficiently calculate average ratings and order by descending average rating
    posts = Post.objects.annotate(average_rating=Avg('ratings__value')).order_by('-average_rating')

    # Add user-specific rating data
    for post in posts:
        user_rating = post.ratings.filter(user=request.user).first()
        post.user_rating = user_rating.value if user_rating else 0  # Store user's rating for each post

    return render(request, 'top_rated.html', {'posts': posts})

@login_required
def profile_view(request):
    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'profile.html', {'user': request.user, 'posts': user_posts})


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True


class SignupView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
    
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful signup
        return render(request, 'signup.html', {'form': form})
