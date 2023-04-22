import random

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from posts.models import Topic, Article


def random_topics(request):
    topics = Topic.objects.filter(is_active=True)
    topics_list = list(topics)

    if topics.count() < 20:
        minimum_count = topics.count()
    elif topics.count() < 1:
        minimum_count = 0
    else:
        minimum_count = 20

    random_topics = random.sample(topics_list, minimum_count)

    return {'random_topics': random_topics}


def trending_topics_list(request):
    latest_articles_for_trending_topics = list(
        set(Article.objects.values_list('topic__title', flat=True).order_by('-created_at')[:100]))

    trending_topics_list = Topic.objects.filter(
        title__in=latest_articles_for_trending_topics, is_active=True).order_by('-created_at')

    return {'trending_topics_list': trending_topics_list}


def articles_objects(request):
    articles = Article.objects.filter(is_active=True).order_by('-created_at')

    paginator = Paginator(articles, per_page=10)
    articles_objects = paginator.get_page(1)
    articles_objects.adjusted_elided_pages = paginator.get_elided_page_range(1)

    return {'articles_objects': articles_objects}
