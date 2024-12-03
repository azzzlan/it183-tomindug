from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.title

    def average_rating(self):
        ratings = self.ratings.all()  # Related name from PostRating
        return sum(rating.value for rating in ratings) / ratings.count() if ratings.exists() else 0

class PostRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    value = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.post.title} - {self.value}"
