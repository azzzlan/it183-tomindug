from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),  # Edit route
    path('post/<int:pk>/rate/', views.rate_post, name='rate_post'),  # Rate route
    path('top-rated/', views.top_rated_posts, name='top_rated'),     # Top Rated route
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
