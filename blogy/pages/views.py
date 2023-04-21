from datetime import datetime
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.text import slugify

from accounts.models import UserModel
from posts.models import Topic, Article, Comment, Like
from posts.forms import CommentForm


def index(request):
    topics = Topic.objects.filter(is_active=True)
    topics_list = list(topics)

    if topics.count() < 20:
        minimum_count = topics.count()
    elif topics.count() < 1:
        minimum_count = 0
    else:
        minimum_count = 20

    random_topics = random.sample(topics_list, minimum_count)

    featured_article = Article.objects.get(is_featured=True)

    articles = Article.objects.filter(is_active=True).order_by('-created_at')

    latest_articles_for_trending_topics = list(
        set(Article.objects.values_list('topic__title', flat=True).order_by('-created_at')[:100]))

    trending_topics_list = Topic.objects.filter(
        title__in=latest_articles_for_trending_topics, is_active=True).order_by('-created_at')

    paginator = Paginator(articles, per_page=10)
    articles_objects = paginator.get_page(1)
    articles_objects.adjusted_elided_pages = paginator.get_elided_page_range(1)

    return render(request, 'pages/index.html', {
        'random_topics': random_topics,
        'featured_article': featured_article,
        'articles_objects': articles_objects,
        'trending_topics_list': trending_topics_list
    })


def index_pages(request, page=1):
    topics = Topic.objects.filter(is_active=True)
    topics_list = list(topics)

    if topics.count() < 20:
        minimum_count = topics.count()
    elif topics.count() < 1:
        minimum_count = 0
    else:
        minimum_count = 20

    random_topics = random.sample(topics_list, minimum_count)

    featured_article = Article.objects.get(is_featured=True)

    articles = Article.objects.filter(is_active=True).order_by('-created_at')

    latest_articles_for_trending_topics = list(
        set(Article.objects.values_list('topic__title', flat=True).order_by('-created_at')[:100]))

    trending_topics_list = Topic.objects.filter(
        title__in=latest_articles_for_trending_topics, is_active=True).order_by('-created_at')

    paginator = Paginator(articles, per_page=10)
    articles_objects = paginator.get_page(page)
    articles_objects.adjusted_elided_pages = paginator.get_elided_page_range(
        page)

    return render(request, 'pages/index.html', {
        'random_topics': random_topics,
        'featured_article': featured_article,
        'articles_objects': articles_objects,
        'trending_topics_list': trending_topics_list
    })


def articles(request):
    articles = Article.objects.filter(is_active=True).order_by('-created_at')

    paginator = Paginator(articles, per_page=10)
    articles_objects = paginator.get_page(1)
    articles_objects.adjusted_elided_pages = paginator.get_elided_page_range(1)

    return render(request, 'pages/articles.html', {'articles_objects': articles_objects})


def articles_pages(request, page=1):
    articles = Article.objects.filter(is_active=True).order_by('-created_at')

    paginator = Paginator(articles, per_page=10)
    articles_objects = paginator.get_page(page)
    articles_objects.adjusted_elided_pages = paginator.get_elided_page_range(
        page)

    return render(request, 'pages/articles.html', {'articles_objects': articles_objects})


def article(request, article_slug):
    article = get_object_or_404(
        Article, slug=article_slug, is_active=True)

    comments_belonging_to_article = Comment.objects.filter(
        article=article, is_active=True).order_by('-updated_at')

    comments_count = comments_belonging_to_article.count()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.title = comment_form.cleaned_data['title']
            comment.slug = slugify(
                comment.title + str(article_slug) + str(datetime.now()), allow_unicode=False
            )
            comment.body = comment_form.cleaned_data['body']
            comment.article = article
            comment.added_by = request.user
            comment.save()

            messages.success(request, comment.title + ' added')

            return redirect('pages:article', article_slug)
        else:
            return HttpResponse('Error', status=400)

    else:
        comment_form = CommentForm()

    return render(request, 'pages/article.html', {
        'article': article,
        'comments_belonging_to_article': comments_belonging_to_article,
        'comments_count': comments_count,
        'comment_form': comment_form
    })


def topics(request):
    topics = Topic.objects.filter(is_active=True).order_by('-created_at')

    return render(request, 'pages/topics.html', {'topics': topics})


def topic(request, topic_slug):
    topic = get_object_or_404(
        Topic, slug=topic_slug, is_active=True)

    articles_belonging_to_topic = Article.objects.filter(
        topic=topic, is_active=True).order_by('-updated_at')

    articles_count = articles_belonging_to_topic.count()

    return render(request, 'pages/topic.html', {
        'topic': topic,
        'articles_belonging_to_topic': articles_belonging_to_topic,
        'articles_count': articles_count
    })


def hot_picks(request):
    # def commented_on_recently(self):
    #     # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    #     self.comment.created_at
    #     now = timezone.now()
    #     return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # now = timezone.now()
    # recently = now - datetime.timedelta(days=1) <= self.pub_date <= now

    # hot_topics = Article.objects.filter(
    #     comment__created_at >= datetime.timedelta(days=1))

    # hot_topics = Article.objects.filter(date__range=[datetime.timedelta(days=1), timezone.now()])

    # comments = Comment.objects.filter(date__range=[datetime.timedelta(days=1), timezone.now()])

    # comments = list(set(Comment.objects.filter(created_at__range=[datetime.timedelta(days=1), timezone.now()])))
    # articles = Article.objects.filter(
    #     created_at__in=comments, is_active=True).order_by('-created_at')

    # startdate = date.today()

    # enddate = startdate + timedelta(days=6)
    # Sample.objects.filter(date__range=[startdate, enddate])

    # comments = Comment.objects.filter(created_at__range=[date.today(), date.today() + timedelta(days=2)])

    latest_comments_for_hot_articles = list(
        set(Comment.objects.values_list('article__title', flat=True).order_by('-created_at')[:100]))

    hot_articles = Article.objects.filter(
        title__in=latest_comments_for_hot_articles, is_active=True).order_by('-created_at')

    return render(request, 'pages/hot_picks.html', {'hot_articles': hot_articles})


def search(request):

    if request.method == 'GET':

        query = request.GET.get('search')

        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(topic__title__icontains=query) |
            Q(topic__description__icontains=query) |
            Q(added_by__name__icontains=query)
        )

        results_count = articles.count()

        paginator = Paginator(articles, per_page=10)
        articles_objects = paginator.get_page(1)
        articles_objects.adjusted_elided_pages = paginator.get_elided_page_range(
            1)

    return render(request, 'pages/search.html', {
        'query': query,
        'articles_objects': articles_objects,
        'results_count': results_count
    })


def search_pages(request, query, page=1):

    articles = Article.objects.filter(
        Q(title__icontains=query) |
        Q(body__icontains=query) |
        Q(topic__title__icontains=query) |
        Q(topic__description__icontains=query) |
        Q(added_by__name__icontains=query)
    )

    results_count = articles.count()

    paginator = Paginator(articles, per_page=10)
    articles_objects = paginator.get_page(page)
    articles_objects.adjusted_elided_pages = paginator.get_elided_page_range(
        page)

    return render(request, 'pages/search.html', {
        'query': query,
        'articles_objects': articles_objects,
        'results_count': results_count
    })


def authors(request):
    authors = UserModel.objects.filter(is_active=True).order_by('-created_at')

    paginator = Paginator(authors, per_page=10)
    authors_objects = paginator.get_page(1)
    authors_objects.adjusted_elided_pages = paginator.get_elided_page_range(1)

    return render(request, 'pages/authors.html', {'authors_objects': authors_objects})


def authors_pages(request, page=1):
    authors = UserModel.objects.filter(is_active=True).order_by('-created_at')

    paginator = Paginator(authors, per_page=10)
    authors_objects = paginator.get_page(page)
    authors_objects.adjusted_elided_pages = paginator.get_elided_page_range(
        page)

    return render(request, 'pages/authors.html', {'authors_objects': authors_objects})


def author(request, username):
    author = get_object_or_404(
        UserModel, username=username, is_active=True)

    topics_by_author = Topic.objects.filter(
        added_by=author, is_active=True).order_by('-updated_at')

    articles_by_author = Article.objects.filter(
        added_by=author, is_active=True).order_by('-updated_at')

    comments_by_author = Comment.objects.filter(
        added_by=author, is_active=True).order_by('-updated_at')

    likes_by_author = Like.objects.filter(
        added_by=author, is_active=True).order_by('-updated_at')

    topics_count = topics_by_author.count()
    articles_count = articles_by_author.count()
    comments_count = comments_by_author.count()
    likes_count = likes_by_author.count()

    return render(request, 'pages/author.html', {
        'author': author,
        'topics_by_author': topics_by_author,
        'articles_by_author': articles_by_author,
        'comments_by_author': comments_by_author,
        'likes_by_author': likes_by_author,
        'topics_count': topics_count,
        'articles_count': articles_count,
        'comments_count': comments_count,
        'likes_count': likes_count
    })


# def reaction_on_article(request, article_slug, reaction):

#     Reaction.objects.filter(
#     product__slug=product_slug, is_product_default=True).update(is_product_default=False)

#     Reaction.objects.filter(
#         slug=product_unit_slug, product__slug=product_slug, is_product_default=False).update(is_product_default=True)


#     return redirect('inventory:view_product', product_slug)

    # article = Article.objects.get(slug=article_slug)
    # reaction_exists = Reaction.objects.filter(
    #     article__slug=article_slug, added_by=request.user, is_active=True).exists()

    #     reaction.type = reaction
    #     reaction.slug = slugify(
    #                 str(reaction.type) + str(article) + str(datetime.now()), allow_unicode=False)
    #             reaction.added_by = request.user

    #             reaction.save()

    #             messages.success(
    #                 request, 'You reacted to this article')
    #             return redirect('pages:article', article_slug)
    #         else:
    #             return HttpResponse('Error handler content', status=400)

    # return render(request, 'pages/article.html', {
    #     'article': article,
    #     'reaction_form': reaction_form
    # })


# def reaction_on_article(request, article_slug):
#     article = Article.objects.get(slug=article_slug)
#     reaction_exists = Reaction.objects.filter(
#         article__slug=article_slug, added_by=request.user, is_active=True).exists()

#     reaction_form = ReactionForm()

#     if request.method == 'POST':
#         if reaction_exists:
#             reaction_form = ReactionForm(instance=reaction, data=request.POST)
#             if reaction_form.is_valid():
#                 reaction_form.save()

#                 return redirect('pages:article', article_slug)

#         else:
#             reaction_form = ReactionForm(request.POST)

#             if reaction_form.is_valid():
#                 reaction = reaction_form.save(commit=False)
#                 reaction.type = request.POST['type']
#                 reaction.slug = slugify(
#                     str(reaction.type) + str(article) + str(datetime.now()), allow_unicode=False)
#                 reaction.added_by = request.user

#                 reaction.save()

#                 messages.success(
#                     request, 'You reacted to this article')
#                 return redirect('pages:article', article_slug)
#             else:
#                 return HttpResponse('Error handler content', status=400)

#     return render(request, 'pages/article.html', {
#         'article': article,
#         'reaction_form': reaction_form
#     })
