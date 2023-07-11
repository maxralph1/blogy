from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify

from accounts.models import UserModel
from posts.models import Topic, Article, Comment


class TopicIndexView(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = UserModel.objects.create(
            username='user2',
            email='user2@user2.com',
            name='User Two',
            password='1234567890'
        )

        topic1 = Topic.objects.create(
            title='This is topic 1',
            slug=slugify('This is topic 1', allow_unicode=False),
            description='This is the description of the topic',
            is_active=True,
            added_by=user,
            updated_at=str(datetime.now())
        )
        topic2 = Topic.objects.create(
            title='This is topic 2',
            slug=slugify('This is topic 2', allow_unicode=False),
            description='This is the description of the topic',
            is_active=True,
            added_by=user,
            updated_at='2023-05-05 16:03:35.299992'
        )
        topic3 = Topic.objects.create(
            title='This is topic 3',
            slug=slugify('This is topic 3', allow_unicode=False),
            description='This is the description of the topic',
            is_active=False,
            added_by=user,
            updated_at='2023-05-05 16:03:35.211992'
        )
        topic4 = Topic.objects.create(
            title='This is topic 4',
            slug=slugify('This is topic 4', allow_unicode=False),
            description='This is the description of the topic',
            is_active=True,
            added_by=user,
            updated_at='2023-05-05 16:03:35.200992'
        )

    def test_view_index(self):
        topic = Topic.objects.filter(is_active=True).order_by('-updated_at')
        self.assertEqual(len(topic), 3)
        response = self.client.get(reverse('posts:topics'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/topics/'))
