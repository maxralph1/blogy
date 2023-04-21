from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    #     path('', views.home, name='home'),


    # Topics
    path('topics/', views.topics, name='topics'),
    path('topics/add/', views.add_topic, name='add_topic'),
    path('topics/<slug:topic_slug>/',
         views.view_topic, name='view_topic'),
    path('topics/<slug:topic_slug>/update/',
         views.update_topic, name='update_topic'),
    path('topics/<slug:topic_slug>/delete/',
         views.delete_topic, name='delete_topic'),


    # Articles
    path('articles/', views.articles, name='articles'),
    path('articles/<int:page>', views.articles_pages, name='articles_pages'),
    path('articles/add/', views.add_article, name='add_article'),
    path('articles/<slug:article_slug>/',
         views.view_article, name='view_article'),
    path('articles/<slug:article_slug>/update/',
         views.update_article, name='update_article'),
    path('articles/<slug:article_slug>/featured/',
         views.set_as_featured_article, name='set_as_featured_article'),
    path('articles/<slug:article_slug>/delete/',
         views.delete_article, name='delete_article'),


    # Authors
    path('authors/', views.authors, name='authors'),
    path('authors/<slug:username>/',
         views.view_author, name='view_author'),
    path('authors/<slug:username>/delete/',
         views.delete_author, name='delete_author'),


    # Comments
    path('comments/', views.comments, name='comments'),
    path('comments/<int:page>', views.comments_pages, name='comments_pages'),
    path('articles/<slug:article_slug>/comments/add/',
         views.add_comment, name='add_comment'),
    path('comments/<slug:comment_slug>/',
         views.view_comment, name='view_comment'),
    path('comments/<slug:comment_slug>/update/',
         views.update_comment, name='update_comment'),
    path('comments/<slug:comment_slug>/delete/',
         views.delete_comment, name='delete_comment'),


    # Likes
    path('likes/', views.likes, name='likes'),
    path('likes/<slug:topic_slug>/',
         views.add_remove_topic_like, name='add_remove_topic_like'),
    path('likes/<slug:article_slug>/',
         views.add_remove_article_like, name='add_remove_article_like'),
    path('likes/<slug:comment_slug>/',
         views.add_remove_comment_like, name='add_remove_comment_like')



    # Reactions
    #     path('reactions/', views.reactions, name='reactions'),
    #     path('reactions/add/', views.add_reaction, name='add_reaction'),
    #     path('reactions/<slug:reaction_slug>/',
    #          views.view_reaction, name='view_reaction'),
    #     path('reactions/<slug:reaction_slug>/update/',
    #          views.update_reaction, name='update_reaction'),
    #     path('reactions/<slug:reaction_slug>/delete/',
    #          views.delete_reaction, name='delete_reaction'),

]
