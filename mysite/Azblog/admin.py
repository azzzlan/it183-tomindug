from django.contrib import admin
from .models import Post, PostRating


class PostRatingInline(admin.TabularInline):
    model = PostRating
    extra = 1  # Allows adding one additional inline entry by default
    readonly_fields = ('user', 'value')  # Makes user and value read-only in the inline
    can_delete = True  # Allow deleting ratings from the inline


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'average_rating', 'total_ratings')  # Fields to display in the admin list view
    list_filter = ('author',)  # Filters by author
    search_fields = ('title', 'content')  # Adds a search bar for title and content
    inlines = [PostRatingInline]  # Adds the PostRating inline
    readonly_fields = ('average_rating',)  # Makes average_rating read-only in the detail view

    def total_ratings(self, obj):
        """Calculate the total number of ratings for the post."""
        return obj.ratings.count()

    total_ratings.short_description = 'Total Ratings'  # Renames the column in the admin list view


@admin.register(PostRating)
class PostRatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'value')  # Fields to display in the admin list view
    list_filter = ('value',)  # Adds a filter for the rating value
    search_fields = ('post__title', 'user__username')  # Adds a search bar for post titles and usernames
