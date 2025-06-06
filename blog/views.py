from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post
from django.core.paginator import Paginator
from .forms import CommentForm


def blog_view(request):
    post_list = Post.objects.all().order_by('-id')
    paginator = Paginator(post_list, 4)
    categories = Category.objects.all()

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'posts': page_obj
    }

    return render(request, 'blog.html', context)


def single_blog_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created_at')
    comment_form = CommentForm()
    related_posts = Post.objects.filter(category=post.category).exclude(pk=post.pk).order_by('-created_at')[:2]

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect('blog', pk=pk)

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'comment_count': comments.count(),
        'related_posts': related_posts,
    }

    return render(request, 'blog-details.html', context)
