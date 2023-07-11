import factory
from accounts.models import UserModel
from posts.models import Topic, Article, Comment, Like
from faker import Faker

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserModel

    username = 'user1'
    email = 'user1@user1.com'
    name = 'User One'
    password = 'tester'
    is_active = True
    is_staff = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if "is_superuser" in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)


class TopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Topic

    title = 'World Events'
    description = 'This is a topi aimed at addressing events around the globe.'
    added_by = factory.SubFactory(UserFactory)


class ArticleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Article

    title = 'This is the first Article'
    body = 'This is the entire body of the lorem of lorem ipsum'
    topic = factory.SubFactory(TopicFactory)
    added_by = factory.SubFactory(UserFactory)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    title = 'This is the first comment'
    body = 'This is the body of the first comment. And every comment belongs to an article.'
    article = factory.SubFactory(ArticleFactory)
    added_by = factory.SubFactory(UserFactory)


class LikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Like

    like_dislike = True
    added_by = factory.SubFactory(UserFactory)
