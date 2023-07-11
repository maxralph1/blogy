# import pytest
# import factory
# from pytest_factoryboy import register


# from tests.factories import UserFactory, TopicFactory, ArticleFactory, CommentFactory, LikeFactory


# register(UserFactory)
# register(TopicFactory)
# register(ArticleFactory)
# register(CommentFactory)
# register(LikeFactory)


# @pytest.fixture
# def user(db, user_factory):
#     user = user_factory.create()
#     return user


# @pytest.fixture
# def topic(db, topic_factory):
#     topic = topic_factory.create()
#     return topic


# @pytest.fixture
# def article(db, article_factory):
#     article = article_factory.create()
#     return article


# @pytest.fixture
# def comment(db, comment_factory):
#     comment = comment_factory.create()
#     return comment


# @pytest.fixture
# def like(db, like_factory):
#     like = like_factory.create()
#     return like
