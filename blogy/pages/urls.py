from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.index, name='index'),
    path('articles/', views.articles, name='articles'),
    path('article/', views.article, name='article'),
    path('about-us/', views.about_us, name='about_us'),
    # path('product/<slug:product_slug>/', views.product, name='product'),
    # path('contact-us/', views.contact_us, name='contact_us'),
]
