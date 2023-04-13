from django.shortcuts import render


def index(request):

    return render(request, 'pages/index.html', {})


def articles(request):

    return render(request, 'pages/articles.html', {})


def article(request):

    return render(request, 'pages/article.html', {})


def about_us(request):

    return render(request, 'pages/about_us.html', {})
