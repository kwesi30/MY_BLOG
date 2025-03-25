from django.urls import path
from .views import (
    BlogListView, BlogDetailView, BlogCreateView, 
    BlogUpdateView, BlogDeleteView, logout_view, 
    SignUpView, CategoryListView
)
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', BlogListView.as_view(), name='home'),
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('post/new/', BlogCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', BlogUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', BlogDeleteView.as_view(), name='post_delete'),

    # Category URLs
    path('category/<slug:category_slug>/', CategoryListView.as_view(), name='category_posts'),

    # Auth URLs
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='website/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
]
