from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category


def index(request):
    """Главная страница с лентой записей."""
    now = timezone.now()

    # Получаем 5 последних опубликованных постов
    post_list = Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=now
    ).select_related(
        'category', 'location', 'author'
    ).order_by('-pub_date')[:5]

    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    """Детальная страница поста."""
    now = timezone.now()

    post = get_object_or_404(
        Post.objects.select_related('category', 'location', 'author'),
        pk=id,
        is_published=True,
        category__is_published=True,
        pub_date__lte=now
    )

    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    """Страница категории."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    now = timezone.now()

    post_list = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=now
    ).select_related(
        'category', 'location', 'author'
    ).order_by('-pub_date')

    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, 'blog/category.html', context)
