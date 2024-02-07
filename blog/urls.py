from django.urls import path
from django.views.decorators.cache import cache_page

from blog.views import BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView, BlogDeleteView

from blog.apps import BlogConfig
app_name = BlogConfig.name

urlpatterns = [
    path('create/', cache_page(60)(BlogCreateView.as_view()), name='create'),
    path('', BlogListView.as_view(), name='blog_list'),
    path('view/<int:pk>/', BlogDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
]