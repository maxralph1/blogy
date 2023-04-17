from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .models import Category, Article, Comment, Reaction
from .forms import CategoryForm, ArticleForm, CommentForm, ReactionForm


# Categories

@login_required
def categories(request):
    categories = Category.objects.filter(added_by=request.user,
                                         is_active=True).order_by('-updated_at')

    return render(request, 'posts/categories/index.html', {'categories': categories})


@login_required
def add_category(request):
    if request.method == 'POST':
        category_form = CategoryForm(request.POST)

        if category_form.is_valid():
            category = category_form.save(commit=False)
            category.title = category_form.cleaned_data['title']
            category.slug = slugify(category.title, allow_unicode=False)
            category.description = category_form.cleaned_data['description']
            category.added_by = request.user
            category.save()

            messages.success(request, category.title + ' added')

            return redirect('accounts:dashboard')
        else:
            return HttpResponse('Error', status=400)

    else:
        category_form = CategoryForm()

    return render(request, 'posts/categories/add.html', {'category_form': category_form})


@login_required
def view_category(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, added_by=request.user, is_active=True)

    articles_belonging_to_category = Article.objects.filter(
        category=category, is_active=True).order_by('-updated_at')

    return render(request, 'posts/categories/category.html', {
        'category': category,
        'articles_belonging_to_category': articles_belonging_to_category
    })


@login_required
def update_category(request, category_slug):
    if request.method == 'POST':
        category = Category.objects.get(
            slug=category_slug, added_by=request.user)
        category_form = CategoryForm(isinstance=category, data=request.POST)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('accounts:dashboard'))

    else:
        category = Category.objects.get(slug=category_slug)
        category_slug = CategoryForm(instance=category)

    return render(request, 'posts/categories/edit.html', {'category': category})


@login_required
def delete_category(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, added_by=request.user, is_active=True)
    category.is_active = False
    category.deleted_at = datetime.now()
    category.save()

    messages.success(request, 'Category removed')

    return redirect('accounts:dashboard')


# Articles

# @login_required
def articles(request):
    # articles = Article.objects.filter(
    #     added_by=request.user, is_active=True).order_by('-updated_at')

    return render(request, 'posts/articles/index.html')
    # return render(request, 'posts/articles/index.html', {'articles': articles})


# @login_required
def add_article(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST, request.FILES)

        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.title = article_form.cleaned_data['title']
            article.category = article_form.cleaned_data['category']
            article.slug = slugify(
                str(article.title) + str(article.category) +
                str(datetime.now()),
                allow_unicode=False
            )
            article.body = article_form.cleaned_data['body']
            article.image = article_form.cleaned_data['image']
            article.added_by = request.user
            article.save()

            messages.success(request, article.title + ' added')

            return redirect('posts:articles')
        else:
            messages.warning(
                request, article.title + ' not added')
            return redirect('posts:add_article')

    else:
        article_form = ArticleForm()

    return render(request, 'posts/articles/add.html', {'article_form': article_form})


# @login_required
def view_article(request, article_slug):
    article = get_object_or_404(
        Article, slug=article_slug, added_by=request.user, is_active=True)

    comments_belonging_to_article = Comment.objects.filter(
        article=article, is_active=True).order_by('-updated_at')

    return render(request, 'posts/articles/article.html', {
        'article': article,
        'comments_belonging_to_article': comments_belonging_to_article
    })


# @login_required
def update_article(request, article_slug):
    article = Article.objects.get(
        slug=article_slug, added_by=request.user, is_active=True)

    if request.method == 'POST':
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


# @login_required
def delete_article(request, article_slug):
    article = get_object_or_404(
        Article, slug=article_slug, added_by=request.user, is_active=True)
    article.is_active = False
    article.deleted_at = datetime.now()
    article.save()

    messages.success(request, 'Article removed')

    return redirect('accounts:dashboard')


# Comments

# @login_required
def comments(request):
    # comments = Comment.objects.filter(
    #     added_by=request.user, is_active=True).order_by('-updated_at')

    return render(request, 'posts/comments/index.html')
    # return render(request, 'posts/comments/index.html', {'comments': comments})


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
                comment.title + article_slug + str(datetime.now()), allow_unicode=False
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
