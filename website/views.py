from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost, Category
from .forms import BlogPostForm

# Home Page - List All Blog Posts
class BlogListView(ListView):
    model = BlogPost
    template_name = 'website/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

# View Individual Blog Post
class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'website/detail.html'
    context_object_name = 'post'

# Create New Blog Post
class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'website/post_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Your blog post has been created successfully!")
        return super().form_valid(form)

# Update Existing Blog Post
class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'website/post_form.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user == self.get_object().author

# Delete Blog Post
class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = 'website/post_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user == self.get_object().author

# List Posts by Category
class CategoryListView(ListView):
    model = BlogPost
    template_name = 'website/category_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return BlogPost.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['category_name'] = get_object_or_404(Category, slug=self.kwargs['category_slug']).name
        return context

# User Sign-Up
class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'website/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Account created successfully! You are now logged in.")
        return super().form_valid(form)

# User Logout
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')
