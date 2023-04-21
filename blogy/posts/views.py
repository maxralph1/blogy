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

from .models import Topic, Article, Comment, Like
from accounts.models import UserModel
from .forms import TopicForm, ArticleForm, CommentForm


# Topics

@login_required
def topics(request):
    topics = Topic.objects.filter(is_active=True).order_by('-updated_at')

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

    articles_count = articles.count()
    paginator = Paginator(articles, per_page=10)
    article_objects = paginator.get_page(1)
    article_objects.adjusted_elided_pages = paginator.get_elided_page_range(1)

    return render(request, 'posts/articles/index.html', {
        'articles': articles,
        'articles_count': articles_count,
        'article_objects': article_objects
    })


@login_required
def articles_pages(request, page=1):
    if request.user.is_staff:
        articles = Article.objects.filter(
            is_active=True).order_by('-updated_at')
    else:
        articles = Article.objects.filter(
            added_by=request.user, is_active=True).order_by('-updated_at')

    paginator = Paginator(articles, per_page=10)
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

            messages.success(request, article.title + ' added.')

            return HttpResponseRedirect(reverse('posts:articles'))
        else:
            messages.warning(
                request, article.title + ' not added')

    else:
        article_form = ArticleForm()

    return render(request, 'posts/articles/add.html', {'article_form': article_form})


@login_required
def view_article(request, article_slug):
    article = get_object_or_404(
        Article, slug=article_slug, is_active=True)

    comments_belonging_to_article = Comment.objects.filter(
        article=article, is_active=True).order_by('-updated_at')

    return render(request, 'posts/articles/article.html', {
        'article': article,
        'comments_belonging_to_article': comments_belonging_to_article
    })


@login_required
def update_article(request, article_slug):
    if request.user.is_staff:
        article = get_object_or_404(
            Article, slug=article_slug, is_active=True)
    else:
        article = get_object_or_404(
            Article, slug=article_slug, added_by=request.user, is_active=True)

    if (request.method == 'POST' and article.added_by == request.user) | (request.method == 'POST' and request.user.is_staff):
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
def set_as_featured_article(request, article_slug):
    Article.objects.filter(is_featured=True).update(is_featured=False)
    Article.objects.filter(article__slug=article_slug,
                           is_featured=False).update(is_featured=True)

    return HttpResponseRedirect(reverse('posts:articles'))


@login_required
def delete_article(request, article_slug):
    if request.user.is_staff:
        article = get_object_or_404(
            Article, slug=article_slug, is_active=True)
    else:
        article = get_object_or_404(
            Article, slug=article_slug, added_by=request.user, is_active=True)

    if (article.added_by != request.user):
        messages.warning(
            request, 'You do not have permissions to remove the article "' + article.title + '".')

    elif (article.added_by == request.user) | (request.user.is_staff == False):
        article.is_active = False
        article.deleted_at = datetime.now()
        article.save()

        messages.success(request, 'Article "' + article.title + '" removed.')

    return HttpResponseRedirect(reverse('posts:articles'))


# Authors

@login_required
def authors(request):
    if request.user.is_staff:
        authors = UserModel.objects.filter(
            is_active=True).order_by('-updated_at')

    return render(request, 'posts/authors/index.html', {'authors': authors})


@login_required
def view_author(request, username):
    author = get_object_or_404(
        UserModel, username=username, is_active=True)

    return render(request, 'posts/authors/author.html', {
        'author': author
    })


@login_required
def delete_author(request, username):
    if request.user.is_staff:
        author = get_object_or_404(
            UserModel, username=username, added_by=request.user, is_active=True)

        author.is_active = False
        author.deleted_at = datetime.now()
        author.save()

        messages.success(request, 'Author' + author.title + ' removed')

        return HttpResponseRedirect(reverse('posts:authors'))


# Comments

@login_required
def comments(request):
    # (my) comments on other authors' articles
    if request.user.is_staff:
        comments_by_me = Comment.objects.filter(
            is_active=True).order_by('-updated_at')
    else:
        comments_by_me = Comment.objects.filter(
            added_by=request.user, is_active=True).order_by('-updated_at')

    paginator = Paginator(comments_by_me, per_page=5)
    comments_by_me_objects = paginator.get_page(1)
    comments_by_me_objects.adjusted_elided_pages = paginator.get_elided_page_range(
        1)

    # comments by others on (my) articles
    comments_by_others_on_my_articles = Comment.objects.exclude(
        added_by=request.user).filter(article__added_by=request.user).order_by('-updated_at')

    paginator2 = Paginator(comments_by_others_on_my_articles, per_page=5)
    comments_by_others_on_my_articles_objects = paginator.get_page(1)
    comments_by_others_on_my_articles_objects.adjusted_elided_pages = paginator2.get_elided_page_range(
        1)

    # general render
    return render(request, 'posts/comments/index.html', {
        'comments_by_me_objects': comments_by_me_objects,
        'comments_by_others_on_my_articles_objects': comments_by_others_on_my_articles_objects
    })


@login_required
def comments_pages(request, page=1):
    # (my) comments on other authors' articles
    if request.user.is_staff:
        comments_by_me = Comment.objects.filter(
            is_active=True).order_by('-updated_at')
    else:
        comments_by_me = Comment.objects.filter(
            added_by=request.user, is_active=True).order_by('-updated_at')

    paginator = Paginator(comments_by_me, per_page=5)
    comments_by_me_objects = paginator.get_page(page)
    comments_by_me_objects.adjusted_elided_pages = paginator.get_elided_page_range(
        page)

    # comments by others on my articles
    comments_by_others_on_my_articles = Comment.objects.exclude(added_by=request.user).filter(
        article__added_by=request.user).order_by('-updated_at')

    paginator2 = Paginator(comments_by_others_on_my_articles, per_page=5)
    comments_by_others_on_my_articles_objects = paginator.get_page(page)
    comments_by_others_on_my_articles_objects.adjusted_elided_pages = paginator2.get_elided_page_range(
        page)

    # general render
    return render(request, 'posts/comments/index.html', {
        'comments_by_me_objects': comments_by_me_objects,
        'comments_by_others_on_my_articles_objects': comments_by_others_on_my_articles_objects
    })


@login_required
def add_comment(request, article_slug):
    article = get_object_or_404(
        Article, slug=article_slug, is_active=True)

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

            return redirect('posts:view_article', article_slug)

    else:
        comment_form = CommentForm()

    return render(request, 'posts/comments/add.html', {
        'article': article,
        'comment_form': comment_form
    })


@login_required
def view_comment(request, comment_slug):
    comment = get_object_or_404(
        Comment, slug=comment_slug, is_active=True)

    return render(request, 'posts/comments/comment.html', {'comment': comment})


@login_required
def update_comment(request, comment_slug):
    if request.user.is_staff:
        comment = get_object_or_404(
            Comment, slug=comment_slug, is_active=True)
    else:
        comment = get_object_or_404(
            Comment, slug=comment_slug, added_by=request.user, is_active=True)

    if (request.method == 'POST' and comment.added_by == request.user) | (request.method == 'POST' and request.user.is_staff):
        comment_form = CommentForm(instance=comment, data=request.POST)
        if comment_form.is_valid():
            comment_form.save()
            return HttpResponseRedirect(reverse('posts:comments'))

    else:
        comment_form = CommentForm(instance=comment)

    return render(request, 'posts/comments/edit.html', {
        'comment': comment,
        'comment_form': comment_form
    })


@login_required
def delete_comment(request, comment_slug):
    if request.user.is_staff:
        comment = get_object_or_404(
            Comment, slug=comment_slug, is_active=True)
    else:
        comment = get_object_or_404(
            Comment, slug=comment_slug, added_by=request.user, is_active=True)

    if (comment.added_by != request.user):
        messages.warning(
            request, 'You do not have permissions to remove ' + comment.title + '.')

    elif (comment.added_by == request.user) | (request.user.is_staff == False):
        comment.is_active = False
        comment.deleted_at = datetime.now()
        comment.save()

        messages.success(request, 'Comment' + comment.title + ' removed')

    return HttpResponseRedirect(reverse('posts:comments'))


# Likes

@login_required
def likes(request):
    if request.user.is_staff:
        topics_likes = Like.objects.filter(like_dislike=True, is_active=True)
        articles_likes = Like.objects.filter(like_dislike=True, is_active=True)
        comments_likes = Like.objects.filter(like_dislike=True, is_active=True)
    else:
        topics_likes = Like.objects.filter(
            like_dislike=True, added_by=request.user, is_active=True)
        articles_likes = Like.objects.filter(
            like_dislike=True, added_by=request.user, is_active=True)
        comments_likes = Like.objects.filter(
            like_dislike=True, added_by=request.user, is_active=True)

    topics_likes_count = topics_likes.count()
    articles_likes_count = articles_likes.count()
    comments_likes_count = comments_likes.count()

    return render(request, 'posts/likes/index.html', {
        'topics_likes': topics_likes,
        'articles_likes': articles_likes,
        'comments_likes': comments_likes,
        'topics_likes_count': topics_likes_count,
        'articles_likes_count': articles_likes_count,
        'comments_likes_count': comments_likes_count
    })


@login_required
def add_remove_topic_like(request, topic_slug):
    like = Like.objects.get(topic__slug=topic_slug, added_by=request.user)

    if like.exists():
        Like.objects.filter(like_dislike=True).update(default=False)
        Like.objects.filter(like_dislike=False).update(default=True)
    else:
        Like.objects.create(
            like_dislike=True,
            slug=slugify(
                str(topic_slug) + str(datetime.now()), allow_unicode=False
            ),
            added_by=request.user
        )

    messages.success(request, 'You reacted on this topic')


@login_required
def add_remove_article_like(request, article_slug):
    like = Like.objects.get(article__slug=article_slug, added_by=request.user)

    if like.exists():
        Like.objects.filter(like_dislike=True).update(default=False)
        Like.objects.filter(like_dislike=False).update(default=True)
    else:
        Like.objects.create(
            like_dislike=True,
            slug=slugify(
                str(article_slug) + str(datetime.now()), allow_unicode=False
            ),
            added_by=request.user
        )

    messages.success(request, 'You reacted on this article')


@login_required
def add_remove_comment_like(request, comment_slug):
    like = Like.objects.get(comment__slug=comment_slug, added_by=request.user)

    if like.exists():
        Like.objects.filter(like_dislike=True).update(default=False)
        Like.objects.filter(like_dislike=False).update(default=True)
    else:
        Like.objects.create(
            like_dislike=True,
            slug=slugify(
                str(comment_slug) + str(datetime.now()), allow_unicode=False
            ),
            added_by=request.user
        )

    messages.success(request, 'You reacted on this comment')


# # Reactions

# @login_required
# def reactions(request):
#     # my comments on other authors' articles
#     if request.user.is_staff:
#         reactions_by_me = Reaction.objects.filter(
#             is_active=True).order_by('-updated_at')

#     else:
#         reactions_by_me = Reaction.objects.filter(
#             added_by=request.user, is_active=True).order_by('-updated_at')

#     paginator = Paginator(reactions_by_me, per_page=5)
#     reactions_by_me_objects = paginator.get_page(1)
#     reactions_by_me_objects.adjusted_elided_pages = paginator.get_elided_page_range(
#         1)

#     # reactions by others on my articles
#     reactions_by_others_on_my_articles = Reaction.objects.filter(
#         article__added_by=request.user).order_by('-updated_at')

#     paginator2 = Paginator(reactions_by_others_on_my_articles, per_page=5)
#     reactions_by_others_on_my_articles_objects = paginator.get_page(1)
#     reactions_by_others_on_my_articles_objects.adjusted_elided_pages = paginator2.get_elided_page_range(
#         1)

#     # if reactions_by_others_on_my_articles.count() > reactions_by_me.count():
#     #     reaction_objects = reactions_by_others_on_my_articles_objects
#     # elif reactions_by_me.count() > reactions_by_others_on_my_articles.count():
#     #     reaction_objects = reaction_by_me_objects

#     # reaction_objects = max(reactions_by_others_on_my_articles_objects.count(), reaction_by_me_objects.count())

#     # general render
#     return render(request, 'posts/reactions/index.html', {
#         'reactions': reactions,
#         # "reaction_objects": reaction_objects,
#         'reactions_by_me_objects': reactions_by_me_objects,
#         'reactions_by_others_on_my_articles_objects': reactions_by_others_on_my_articles_objects
#     })


# @login_required
# def reactions_pages(request, page=1):
#     # my reactions on other authors' articles
#     if request.user.is_staff:
#         reactions_by_me = Reaction.objects.filter(
#             is_active=True).order_by('-updated_at')

#     else:
#         reactions_by_me = Reaction.objects.filter(
#             added_by=request.user, is_active=True).order_by('-updated_at')

#     paginator = Paginator(reactions_by_me, per_page=2)
#     reactions_by_me_objects = paginator.get_page(page)
#     reactions_by_me_objects.adjusted_elided_pages = paginator.get_elided_page_range(
#         page)

#     # reactions by others on my articles
#     reactions_by_others_on_my_articles = Reaction.objects.filter(
#         article__added_by=request.user).order_by('-updated_at')

#     paginator2 = Paginator(reactions_by_others_on_my_articles, per_page=5)
#     reactions_by_others_on_my_articles_objects = paginator.get_page(page)
#     reactions_by_others_on_my_articles_objects.adjusted_elided_pages = paginator2.get_elided_page_range(
#         page)

#     # if reactions_by_others_on_my_articles.count() > reactions_by_me.count():
#     #     reaction_objects = reactions_by_others_on_my_articles_objects.adjusted_elided_pages
#     # elif reactions_by_me.count() > reactions_by_others_on_my_articles.count():
#     #     reaction_objects = reaction_by_me_objects.adjusted_elided_pages

#     # reaction_objects = max(reactions_by_others_on_my_articles_objects.count(), reaction_by_me_objects.count())

#     # general render
#     return render(request, 'posts/reactions/index.html', {
#         'reactions': reactions,
#         # "reaction_objects": reaction_objects,
#         'reactions_by_me_objects': reactions_by_me_objects,
#         'reactions_by_others_on_my_articles_objects': reactions_by_others_on_my_articles_objects
#     })


# @login_required
# def add_update_article_reaction(request, article_slug):
#     reaction = Reaction.objects.get(slug=article_slug, added_by=request.user)

#     if request.method == 'POST':
#         if reaction is not None:
#             reaction.type = reaction_form.cleaned_data['type']
#             reaction.save()

#             return redirect('posts:article', article_slug)
#         else:
#             article = Article.objects.get(
#                 article__slug=article_slug, added_by=request.user)

#             reaction.type = reaction_form.cleaned_data['type']
#             reaction.article = article.id
#             reaction.added_by = request.user
#             reaction.save()

#             return redirect('posts:article', article_slug)
#     else:
#         reaction_form = ReactionForm()

#     return render(request, 'posts/articles/article.html', {'reaction_form': reaction_form})


# @login_required
# def add_update_comment_reaction(request, comment_slug):
#     reaction = Reaction.objects.get(slug=comment_slug, added_by=request.user)

#     if request.method == 'POST':
#         if reaction is not None:
#             reaction.type = reaction_form.cleaned_data['type']
#             reaction.save()

#             return redirect('posts:comment', comment_slug)
#         else:
#             comment = Comment.objects.get(
#                 comment__slug=comment_slug, added_by=request.user)

#             reaction.type = reaction_form.cleaned_data['type']
#             reaction.comment = comment.id
#             reaction.added_by = request.user
#             reaction.save()

#             return redirect('posts:comment', comment_slug)
#     else:
#         reaction_form = ReactionForm()

#     return render(request, 'posts/comments/comment.html', {'reaction_form': reaction_form})
