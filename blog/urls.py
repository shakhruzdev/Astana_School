from django.urls import path
from .views import blog_view, single_blog_view

urlpatterns = [
    path('blog/', blog_view, name='blog_list'),
    path('blog/<int:pk>/', single_blog_view, name='blog'),
]
