from datetime import datetime
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .models import Topic, Article, Comment, Reaction
from accounts.models import UserModel
from .forms import TopicForm, ArticleForm, CommentForm, ReactionForm


# Topics

@login_required
def topics(request):
    topics = Topic.objects.filter(is_active=True).order_by('-updated_at')
    # topics = Topic.objects.filter(added_by=request.user,
    #                               is_active=True).order_by('-updated_at')

    return render(request, 'posts/topics/index.html', {'topics': topics})


@login_required
def add_topic(request):
    if request.method == 'POST':
        topic_form = TopicForm(request.POST)

        if topic_form.is_valid():
            topic = topic_form.save(commit=False)
            topic.title = topic_form.cleaned_data['title']
            topic.slug = slugify(topic.title, allow_unicode=False)
            topic.description = topic_form.cleaned_data['description']
            topic.representative_color = random.choice(
                ['primary', 'secondary', 'success', 'info', 'warning', 'danger'])
            topic.added_by = request.user
            topic.save()

            messages.success(request, topic.title + ' added')

            return HttpResponseRedirect(reverse('posts:topics'))
        else:
            return HttpResponse('Error', status=400)

    else:
        topic_form = TopicForm()

    return render(request, 'posts/topics/add.html', {'topic_form': topic_form})


@login_required
def view_topic(request, topic_slug):
    topic = get_object_or_404(
        Topic, slug=topic_slug, is_active=True)

    articles_belonging_to_topic = Article.objects.filter(
        topic=topic, is_active=True).order_by('-updated_at')

    return render(request, 'posts/topics/topic.html', {
        'topic': topic,
        'articles_belonging_to_topic': articles_belonging_to_topic
    })


@login_required
def update_topic(request, topic_slug):
    topic = get_object_or_404(
        Topic, slug=topic_slug, added_by=request.user, is_active=True)

    if request.method == 'POST' and topic.added_by == request.user:
        topic_form = TopicForm(instance=topic, data=request.POST)
        if topic_form.is_valid():
            topic_form.save()
            return HttpResponseRedirect(reverse('posts:topics'))

    else:
        topic_form = TopicForm(instance=topic)

    return render(request, 'posts/topics/edit.html', {
        'topic': topic,
        'topic_form': topic_form
    })


@login_required
def delete_topic(request, topic_slug):
    topic = get_object_or_404(
        Topic, slug=topic_slug, added_by=request.user, is_active=True)

    if topic.added_by != request.user:
        messages.warning(request, topic.title + ' cannot be removed by you.')

        return HttpResponseRedirect(reverse('posts:topics'))

    else:
        topic.is_active = False
        topic.deleted_at = datetime.now()
        topic.save()

        messages.warning(request, 'Topic removed')

        return HttpResponseRedirect(reverse('posts:topics'))


# Articles

def articles(request):
    if request.user.is_staff:
        articles = Article.objects.filter(
            is_active=True).order_by('-updated_at')
    else:
        articles = Article.objects.filter(
            added_by=request.user, is_active=True).order_by('-updated_at')

    paginator = Paginator(articles, per_page=2)
    article_objects = paginator.get_page(1)
    article_objects.adjusted_elided_pages = paginator.get_elided_page_range(1)

    return render(request, 'posts/articles/index.html', {
        'articles': articles,
        "article_objects": article_objects
    })


@login_required
def articles_pages(request, page=1):
    # articles = Article.objects.filter(
    #     added_by=request.user, is_active=True).order_by('-updated_at')

    # return render(request, 'posts/articles/index.html')
    # # return render(request, 'posts/articles/index.html', {'articles': articles})

    # topics = Topic.objects.filter(is_active=True).order_by('-updated_at')
    # # topics = Topic.objects.filter(added_by=request.user,
    # #                               is_active=True).order_by('-updated_at')

    # return render(request, 'posts/topics/index.html', {'topics': topics})

    if request.user.is_staff:
        articles = Article.objects.filter(
            is_active=True).order_by('-updated_at')
    else:
        articles = Article.objects.filter(
            added_by=request.user, is_active=True).order_by('-updated_at')

    paginator = Paginator(articles, per_page=2)
    article_objects = paginator.get_page(page)
    article_objects.adjusted_elided_pages = paginator.get_elided_page_range(
        page)

    return render(request, 'posts/articles/index.html', {'article_objects': article_objects})


@login_required
def add_article(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)

        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.title = article_form.cleaned_data['title']
            article.topic = article_form.cleaned_data['topic']
            article.slug = slugify(
                str(article.title) + str(article.topic) +
                str(datetime.now()),
                allow_unicode=False
            )
            article.body = article_form.cleaned_data['body']
            article.image = article_form.cleaned_data['image']
            article.added_by = request.user
            article.save()

            messages.success(request, article.title + ' added')

            return HttpResponseRedirect(reverse('posts:articles'))
        else:
            messages.warning(
                request, article.title + ' not added')
            return redirect('posts:add_article')

    else:
        article_form = ArticleForm()

    return render(request, 'posts/articles/add.html', {'article_form': article_form})


@login_required
def view_article(request, article_slug):
    if request.user.is_staff:
        article = get_object_or_404(
            Article, slug=article_slug, is_active=True)
    else:
        article = get_object_or_404(
            Article, slug=article_slug, added_by=request.user, is_active=True)

    comments_belonging_to_article = Comment.objects.filter(
        article=article, is_active=True).order_by('-updated_at')

    return render(request, 'posts/articles/article.html', {
        'article': article,
        'comments_belonging_to_article': comments_belonging_to_article
    })


@login_required
def update_article(request, article_slug):
    article = Article.objects.get(
        slug=article_slug, added_by=request.user, is_active=True)

    if request.method == 'POST' and article.added_by == request.user:
        article_form = ArticleForm(instance=article, data=request.POST)
        if article_form.is_valid():
            article_form.save()
            return HttpResponseRedirect(reverse('posts:articles'))

    else:
        article_form = ArticleForm(instance=article)

    return render(request, 'posts/articles/edit.html', {
        'article': article,
        'article_form': article_form
    })


@login_required
def delete_article(request, article_slug):
    article = get_object_or_404(
        Article, slug=article_slug, added_by=request.user, is_active=True)

    if article.added_by != request.user:
        messages.warning(
            request, 'You do not have permissions to remove ' + article.title + '.')

    else:
        article.is_active = False
        article.deleted_at = datetime.now()
        article.save()

        messages.success(request, 'Article' + article.title + ' removed')

    return HttpResponseRedirect(reverse('posts:articles'))


@login_required
def authors(request):
    if request.user.is_staff:
        authors = UserModel.objects.filter(
            is_active=True).order_by('-updated_at')

    return render(request, 'posts/authors/index.html', {'authors': authors})


@login_required
def view_author(request, author_slug):
    if request.user.is_staff:
        author = get_object_or_404(
            UserModel, slug=author_slug, is_active=True)

    return render(request, 'posts/authors/author.html', {
        'author': author
    })


@login_required
def delete_author(request, author_slug):
    if request.user.is_staff:
        author = get_object_or_404(
            UserModel, slug=author_slug, added_by=request.user, is_active=True)

        author.is_active = False
        author.deleted_at = datetime.now()
        author.save()

        messages.success(request, 'Author' + author.title + ' removed')

        return HttpResponseRedirect(reverse('posts:authors'))


# Comments

@login_required
def comments(request):
    if request.user.is_staff:
        comments = Comment.objects.filter(
            is_active=True).order_by('-updated_at')
    else:
        comments = Comment.objects.filter(
            added_by=request.user, is_active=True).order_by('-updated_at')

    paginator = Paginator(comments, per_page=2)
    comment_objects = paginator.get_page(1)
    comment_objects.adjusted_elided_pages = paginator.get_elided_page_range(1)

    return render(request, 'posts/comments/index.html', {
        'comments': comments,
        "comment_objects": comment_objects
    })


@login_required
def add_comment(request, article_slug):
    if request.method == 'POST':
        article = Article.objects.get(
            article__slug=article_slug, is_active=True)

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.title = comment_form.cleaned_data['title']
            comment.slug = slugify(
                comment.title + str(article_slug) + str(datetime.now()), allow_unicode=False
            )
            comment.body = comment_form.cleaned_data['body']
            comment.article = article.id
            comment.added_by = request.user
            comment.save()

            messages.success(request, comment.title + ' added')

    else:
        comment_form = CommentForm()

    return render(request, 'posts/articles/article.html', {'comment_form': comment_form})


@login_required
def view_comment(request, comment_slug):
    comment = get_object_or_404(
        comment, slug=comment_slug, added_by=request.user, is_active=True)

    return render(request, 'posts/comments/comment.html', {'comment': comment})


@login_required
def update_comment(request, comment_slug):
    if request.method == 'POST':
        comment = Comment.objects.get(added_by=request.user, slug=comment_slug)
        comment_form = CommentForm(instance=comment, data=request.POST)

        if comment_form.is_valid():
            comment_form.save()
            return HttpResponseRedirect(reverse('post:articles'))


@login_required
def delete_comment(request, comment_slug):
    comment = get_object_or_404(
        Comment, slug=comment_slug, added_by=request.user, is_active=True)
    comment.is_active = False
    comment.deleted_at = datetime.now()
    comment.save()

    messages.success(request, 'Comment removed')

    return redirect('accounts:dashboard')


# Reactions

@login_required
def reactions(request):
    pass


@login_required
def add_update_article_reaction(request, article_slug):
    reaction = Reaction.objects.get(slug=article_slug, added_by=request.user)

    if request.method == 'POST':
        if reaction is not None:
            reaction.type = reaction_form.cleaned_data['type']
            reaction.save()

            return redirect('posts:article', article_slug)
        else:
            article = Article.objects.get(
                article__slug=article_slug, added_by=request.user)

            reaction.type = reaction_form.cleaned_data['type']
            reaction.article = article.id
            reaction.added_by = request.user
            reaction.save()

            return redirect('posts:article', article_slug)
    else:
        reaction_form = ReactionForm()

    return render(request, 'posts/articles/article.html', {'reaction_form': reaction_form})


@login_required
def add_update_comment_reaction(request, comment_slug):
    reaction = Reaction.objects.get(slug=comment_slug, added_by=request.user)

    if request.method == 'POST':
        if reaction is not None:
            reaction.type = reaction_form.cleaned_data['type']
            reaction.save()

            return redirect('posts:comment', comment_slug)
        else:
            comment = Comment.objects.get(
                comment__slug=comment_slug, added_by=request.user)

            reaction.type = reaction_form.cleaned_data['type']
            reaction.comment = comment.id
            reaction.added_by = request.user
            reaction.save()

            return redirect('posts:comment', comment_slug)
    else:
        reaction_form = ReactionForm()

    return render(request, 'posts/comments/comment.html', {'reaction_form': reaction_form})
