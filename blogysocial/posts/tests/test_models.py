from datetime import datetime

from django.test import TestCase
from django.utils.text import slugify

from accounts.models import UserModel
from posts.models import Topic, Article, Comment, Like


class TopicModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = UserModel.objects.create(
            username='user2',
            email='user2@user2.com',
            name='User Two',
            password='1234567890'
        )

        Topic.objects.create(
            title='First Topic',
            slug=slugify('First Topic', allow_unicode=False),
            description='This is the first topic.',
            added_by=user
        )

    def test_title_verbose_name(self):
        topic = Topic.objects.get(slug='first-topic')
        verbose_name = topic._meta.get_field('title').verbose_name
        self.assertEqual(verbose_name, 'Topic Title')

    def test_slug_verbose_name(self):
        topic = Topic.objects.get(slug='first-topic')
        verbose_name = topic._meta.get_field('slug').verbose_name
        self.assertEqual(verbose_name, 'Topic safe URL')

    def test_description_verbose_name(self):
        topic = Topic.objects.get(slug='first-topic')
        verbose_name = topic._meta.get_field('description').verbose_name
        self.assertEqual(verbose_name, 'Topic Description')

    def test_representative_color_verbose_name(self):
        topic = Topic.objects.get(slug='first-topic')
        verbose_name = topic._meta.get_field(
            'representative_color').verbose_name
        self.assertEqual(verbose_name, 'Representive Color for Topic')

    def test_is_active_verbose_name(self):
        topic = Topic.objects.get(slug='first-topic')
        verbose_name = topic._meta.get_field(
            'is_active').verbose_name
        self.assertEqual(verbose_name, 'Topic visibility')

    def test_created_at_verbose_name(self):
        topic = Topic.objects.get(slug='first-topic')
        verbose_name = topic._meta.get_field(
            'created_at').verbose_name
        self.assertEqual(verbose_name, 'Created at')

    def test_updated_at_verbose_name(self):
        topic = Topic.objects.get(slug='first-topic')
        verbose_name = topic._meta.get_field(
            'updated_at').verbose_name
        self.assertEqual(verbose_name, 'Updated at')

    def test_deleted_at_verbose_name(self):
        topic = Topic.objects.get(slug='first-topic')
        verbose_name = topic._meta.get_field(
            'deleted_at').verbose_name
        self.assertEqual(verbose_name, 'Deleted at')

    def test_title_help_text(self):
        topic = Topic.objects.get(slug='first-topic')
        help_text = topic._meta.get_field('title').help_text
        self.assertEqual(help_text, 'Required and unique')

    def test_description_help_text(self):
        topic = Topic.objects.get(slug='first-topic')
        help_text = topic._meta.get_field('description').help_text
        self.assertEqual(help_text, 'Required and unique')

    def test_representative_color_help_text(self):
        topic = Topic.objects.get(slug='first-topic')
        help_text = topic._meta.get_field('representative_color').help_text
        self.assertEqual(
            help_text, 'Color for display of Topic to site visitors')

    def test_is_active_help_text(self):
        topic = Topic.objects.get(slug='first-topic')
        help_text = topic._meta.get_field('is_active').help_text
        self.assertEqual(help_text, 'Change topic visibility')

    def test_title_max_length(self):
        topic = Topic.objects.get(slug='first-topic')
        max_length = topic._meta.get_field('title').max_length
        self.assertEqual(max_length, 30)

    def test_slug_max_length(self):
        topic = Topic.objects.get(slug='first-topic')
        max_length = topic._meta.get_field('slug').max_length
        self.assertEqual(max_length, 255)

    def test_description_max_length(self):
        topic = Topic.objects.get(slug='first-topic')
        max_length = topic._meta.get_field('description').max_length
        self.assertEqual(max_length, 255)

    def test_representative_color_max_length(self):
        topic = Topic.objects.get(slug='first-topic')
        max_length = topic._meta.get_field('representative_color').max_length
        self.assertEqual(max_length, 10)

    def test_title_unique(self):
        topic = Topic.objects.get(slug='first-topic')
        unique = topic._meta.get_field('title').unique
        self.assertEqual(unique, True)

    def test_slug_unique(self):
        topic = Topic.objects.get(slug='first-topic')
        unique = topic._meta.get_field('slug').unique
        self.assertEqual(unique, True)

    def test_representative_color_default(self):
        topic = Topic.objects.get(slug='first-topic')
        default = topic._meta.get_field('representative_color').default
        self.assertEqual(default, 'secondary')

    def test_is_active_default(self):
        topic = Topic.objects.get(slug='first-topic')
        default = topic._meta.get_field('is_active').default
        self.assertEqual(default, True)

    def test_created_at_auto_now_add(self):
        topic = Topic.objects.get(slug='first-topic')
        auto_now_add = topic._meta.get_field('created_at').auto_now_add
        self.assertEqual(auto_now_add, True)

    def test_updated_at_auto_now(self):
        topic = Topic.objects.get(slug='first-topic')
        auto_now = topic._meta.get_field('updated_at').auto_now
        self.assertEqual(auto_now, True)

    def test_created_at_editable(self):
        topic = Topic.objects.get(slug='first-topic')
        editable = topic._meta.get_field('created_at').editable
        self.assertEqual(editable, False)

    def test_deleted_at_null(self):
        topic = Topic.objects.get(slug='first-topic')
        null = topic._meta.get_field('deleted_at').null
        self.assertEqual(null, True)

    def test_deleted_at_blank(self):
        topic = Topic.objects.get(slug='first-topic')
        blank = topic._meta.get_field('deleted_at').blank
        self.assertEqual(blank, True)

    def test_get_absolute_url(self):
        topic = Topic.objects.get(slug='first-topic')
        self.assertEqual(topic.get_absolute_url(),
                         '/posts/topics/first-topic/')

    def test_object_str_is_title(self):
        topic = Topic.objects.get(slug='first-topic')
        expected_object = topic.title
        self.assertEqual(str(topic), expected_object)


class ArticleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        topic_user = UserModel.objects.create(
            username='topicuser',
            email='topicuser@topicuser.com',
            name='Topic User',
            password='1234567890'
        )
        topic = Topic.objects.create(
            title='Topic for Article',
            description='This is the topic for article test.',
            added_by=topic_user
        )
        user = UserModel.objects.create(
            username='user2',
            email='user2@user2.com',
            name='User Two',
            password='1234567890'
        )
        Article.objects.create(
            title='First Article',
            slug=slugify('First Article' +
                         topic.title, allow_unicode=False),
            #    slug=slugify(
            #        'First Article' + topic.title + str(datetime.now()), allow_unicode=False),
            body='This is the first article.',
            topic=topic,
            added_by=user
        )

    def test_is_featured_verbose_name(self):
        article = Article.objects.get(id=1)
        verbose_name = article._meta.get_field('is_featured').verbose_name
        self.assertEqual(verbose_name, 'Make Article Featured')

    def test_title_verbose_name(self):
        article = Article.objects.get(id=1)
        verbose_name = article._meta.get_field('title').verbose_name
        self.assertEqual(verbose_name, 'Article Title')

    def test_slug_verbose_name(self):
        article = Article.objects.get(id=1)
        verbose_name = article._meta.get_field('slug').verbose_name
        self.assertEqual(verbose_name, 'Article safe URL')

    def test_body_verbose_name(self):
        article = Article.objects.get(id=1)
        verbose_name = article._meta.get_field('body').verbose_name
        self.assertEqual(verbose_name, 'Write your Article')

    def test_image_verbose_name(self):
        article = Article.objects.get(id=1)
        verbose_name = article._meta.get_field('image').verbose_name
        self.assertEqual(verbose_name, 'Article Preview Image')

    def test_topic_verbose_name(self):
        article = Article.objects.get(id=1)
        verbose_name = article._meta.get_field('topic').verbose_name
        self.assertEqual(verbose_name, 'Choose a Topic')

    def test_is_active_verbose_name(self):
        article = Article.objects.get(id=1)
        verbose_name = article._meta.get_field('is_active').verbose_name
        self.assertEqual(verbose_name, 'Topic visibility')

    def test_created_at_verbose_name(self):
        article = Article.objects.get(id=1)
        verbose_name = article._meta.get_field('created_at').verbose_name
        self.assertEqual(verbose_name, 'Created at')

    def test_updated_at_verbose_name(self):
        article = Article.objects.get(id=1)
        verbose_name = article._meta.get_field('updated_at').verbose_name
        self.assertEqual(verbose_name, 'Updated at')

    def test_is_featured_help_text(self):
        article = Article.objects.get(id=1)
        help_text = article._meta.get_field('is_featured').help_text
        self.assertEqual(
            help_text, 'Change make article featured on index(home) page')

    def test_title_help_text(self):
        article = Article.objects.get(id=1)
        help_text = article._meta.get_field('title').help_text
        self.assertEqual(help_text, 'Required and unique')

    def test_image_help_text(self):
        article = Article.objects.get(id=1)
        help_text = article._meta.get_field('image').help_text
        self.assertEqual(help_text, 'Upload Article Image')

    def test_is_active_help_text(self):
        article = Article.objects.get(id=1)
        help_text = article._meta.get_field('is_active').help_text
        self.assertEqual(help_text, 'Change topic visibility')

    def test_title_max_length(self):
        article = Article.objects.get(id=1)
        max_length = article._meta.get_field('title').max_length
        self.assertEqual(max_length, 150)

    def test_slug_max_length(self):
        article = Article.objects.get(id=1)
        max_length = article._meta.get_field('slug').max_length
        self.assertEqual(max_length, 255)

    def test_slug_unique(self):
        article = Article.objects.get(id=1)
        unique = article._meta.get_field('slug').unique
        self.assertEqual(unique, True)

    def test_body_unique(self):
        article = Article.objects.get(id=1)
        unique = article._meta.get_field('body').unique
        self.assertEqual(unique, True)

    def test_is_featured_default(self):
        article = Article.objects.get(id=1)
        default = article._meta.get_field('is_featured').default
        self.assertEqual(default, False)

    def test_image_default(self):
        article = Article.objects.get(id=1)
        default = article._meta.get_field('image').default
        self.assertEqual(default, 'images/default.png')

    def test_is_active_default(self):
        article = Article.objects.get(id=1)
        default = article._meta.get_field('is_active').default
        self.assertEqual(default, True)

    def test_image_upload_to(self):
        article = Article.objects.get(id=1)
        upload_to = article._meta.get_field('image').upload_to
        self.assertEqual(upload_to, 'images/articles/')

    def test_created_at_auto_now_add(self):
        article = Article.objects.get(id=1)
        auto_now_add = article._meta.get_field('created_at').auto_now_add
        self.assertEqual(auto_now_add, True)

    def test_updated_at_auto_now(self):
        article = Article.objects.get(id=1)
        auto_now = article._meta.get_field('updated_at').auto_now
        self.assertEqual(auto_now, True)

    def test_created_at_editable(self):
        article = Article.objects.get(id=1)
        editable = article._meta.get_field('created_at').editable
        self.assertEqual(editable, False)

    def test_deleted_at_null(self):
        article = Article.objects.get(id=1)
        null = article._meta.get_field('deleted_at').null
        self.assertEqual(null, True)

    def test_deleted_at_blank(self):
        article = Article.objects.get(id=1)
        blank = article._meta.get_field('deleted_at').blank
        self.assertEqual(blank, True)

    def test_get_absolute_url(self):
        article = Article.objects.get(id=1)
        self.assertEqual(article.get_absolute_url(),
                         '/posts/articles/' + slugify('First Article' + 'Topic for Article' + '/', allow_unicode=False) + '/')

    # The milliseconds delay in time between creating the test db sample and creating the actual testing causes a minor difference in the slug generated, as the datetime python package is used to generate unique slug for each article to help promote more uniqueness and avoid future database clashes of possible repeated entries
    # Here is a sample of the difference from the python shell
    # - /posts/articles/first-articletopic-for-article2023-04-23-141759450033/
    # ?                                                                 ^^^^^
    # + /posts/articles/first-articletopic-for-article2023-04-23-141759476646/
    # ?                                                                 ^^^^^
    # def test_get_absolute_url(self):
    #     article = Article.objects.get(id=1)
    #     self.assertEqual(article.get_absolute_url(),
    #                      '/posts/articles/' + format(slugify(
    #                          'First Article' + 'Topic for Article' + str(datetime.now()), allow_unicode=False)) + '/')

    def test_object_str_is_title(self):
        article = Article.objects.get(id=1)
        expected_object = article.title
        self.assertEqual(str(article), expected_object)


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = UserModel.objects.create(
            username='user2',
            email='user2@user2.com',
            name='User Two',
            password='1234567890'
        )
        topic = Topic.objects.create(
            title='Test Topic',
            description='This is a test topic.',
            added_by=user
        )
        article = Article.objects.create(
            title='Test Article',
            body='This is a test article.',
            topic=topic,
            added_by=user
        )
        Comment.objects.create(
            title='First Comment',
            slug=slugify('First Comment' +
                         article.title, allow_unicode=False),
            body='This is the first comment.',
            article=article,
            added_by=user
        )

    def test_title_verbose_name(self):
        comment = Comment.objects.get(id=1)
        verbose_name = comment._meta.get_field('title').verbose_name
        self.assertEqual(verbose_name, 'Comment Title')

    def test_slug_verbose_name(self):
        comment = Comment.objects.get(id=1)
        verbose_name = comment._meta.get_field('slug').verbose_name
        self.assertEqual(verbose_name, 'Comment safe URL')

    def test_body_verbose_name(self):
        comment = Comment.objects.get(id=1)
        verbose_name = comment._meta.get_field('body').verbose_name
        self.assertEqual(verbose_name, 'Comment Body')

    def test_is_active_verbose_name(self):
        comment = Comment.objects.get(id=1)
        verbose_name = comment._meta.get_field('is_active').verbose_name
        self.assertEqual(verbose_name, 'Comment visibility')

    def test_created_at_verbose_name(self):
        comment = Comment.objects.get(id=1)
        verbose_name = comment._meta.get_field('created_at').verbose_name
        self.assertEqual(verbose_name, 'Created at')

    def test_updated_at_verbose_name(self):
        comment = Comment.objects.get(id=1)
        verbose_name = comment._meta.get_field('updated_at').verbose_name
        self.assertEqual(verbose_name, 'Updated at')

    def test_title_help_text(self):
        comment = Comment.objects.get(id=1)
        help_text = comment._meta.get_field('title').help_text
        self.assertEqual(help_text, 'Comment Title')

    def test_body_help_text(self):
        comment = Comment.objects.get(id=1)
        help_text = comment._meta.get_field('body').help_text
        self.assertEqual(help_text, 'Message must not exceed 255 characters')

    def test_is_active_help_text(self):
        comment = Comment.objects.get(id=1)
        help_text = comment._meta.get_field('is_active').help_text
        self.assertEqual(help_text, 'Change comment visibility')

    def test_title_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('title').max_length
        self.assertEqual(max_length, 255)

    def test_slug_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('slug').max_length
        self.assertEqual(max_length, 255)

    def test_body_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('body').max_length
        self.assertEqual(max_length, 255)

    def test_slug_unique(self):
        comment = Comment.objects.get(id=1)
        unique = comment._meta.get_field('slug').unique
        self.assertEqual(unique, True)

    def test_is_active_default(self):
        comment = Comment.objects.get(id=1)
        default = comment._meta.get_field('is_active').default
        self.assertEqual(default, True)

    def test_created_at_auto_now_add(self):
        comment = Comment.objects.get(id=1)
        auto_now_add = comment._meta.get_field('created_at').auto_now_add
        self.assertEqual(auto_now_add, True)

    def test_updated_at_auto_now(self):
        comment = Comment.objects.get(id=1)
        auto_now = comment._meta.get_field('updated_at').auto_now
        self.assertEqual(auto_now, True)

    def test_created_at_editable(self):
        comment = Comment.objects.get(id=1)
        editable = comment._meta.get_field('created_at').editable
        self.assertEqual(editable, False)

    def test_deleted_at_null(self):
        comment = Comment.objects.get(id=1)
        null = comment._meta.get_field('deleted_at').null
        self.assertEqual(null, True)

    def test_deleted_at_blank(self):
        comment = Comment.objects.get(id=1)
        blank = comment._meta.get_field('deleted_at').blank
        self.assertEqual(blank, True)


class LikeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = UserModel.objects.create(
            username='user2',
            email='user2@user2.com',
            name='User Two',
            password='1234567890'
        )
        topic = Topic.objects.create(
            title='Test Topic',
            description='This is a test topic.',
            added_by=user
        )
        article = Article.objects.create(
            title='Test Article',
            body='This is a test article.',
            topic=topic,
            added_by=user
        )
        # comment = Comment.objects.create(title='Test Comment',
        #                                  body='This is a test comment.',
        #                                  #  topic=topic,
        #                                  article=article,
        #                                  added_by=user)
        Like.objects.create(
            like_dislike=True,
            slug=slugify(article.title, allow_unicode=False),
            article=article,
            added_by=user
        )

    def test_like_dislike_verbose_name(self):
        like = Like.objects.get(id=1)
        verbose_name = like._meta.get_field('like_dislike').verbose_name
        self.assertEqual(verbose_name, 'Like/Dislike')

    def test_slug_verbose_name(self):
        like = Like.objects.get(id=1)
        verbose_name = like._meta.get_field('slug').verbose_name
        self.assertEqual(verbose_name, 'Like safe URL')

    def test_is_active_verbose_name(self):
        like = Like.objects.get(id=1)
        verbose_name = like._meta.get_field('is_active').verbose_name
        self.assertEqual(verbose_name, 'Like visibility')

    def test_created_at_verbose_name(self):
        like = Like.objects.get(id=1)
        verbose_name = like._meta.get_field('created_at').verbose_name
        self.assertEqual(verbose_name, 'Created at')

    def test_updated_at_verbose_name(self):
        like = Like.objects.get(id=1)
        verbose_name = like._meta.get_field('updated_at').verbose_name
        self.assertEqual(verbose_name, 'Updated at')

    def test_like_dislike_help_text(self):
        like = Like.objects.get(id=1)
        help_text = like._meta.get_field('like_dislike').help_text
        self.assertEqual(help_text, 'Like/Dislike')

    def test_is_active_help_text(self):
        like = Like.objects.get(id=1)
        help_text = like._meta.get_field('is_active').help_text
        self.assertEqual(help_text, 'Change like visibility')

    def test_slug_unique(self):
        like = Like.objects.get(id=1)
        unique = like._meta.get_field('slug').unique
        self.assertEqual(unique, True)

    def test_is_active_default(self):
        like = Like.objects.get(id=1)
        default = like._meta.get_field('is_active').default
        self.assertEqual(default, True)

    def test_created_at_auto_now_add(self):
        like = Like.objects.get(id=1)
        auto_now_add = like._meta.get_field('created_at').auto_now_add
        self.assertEqual(auto_now_add, True)

    def test_updated_at_auto_now(self):
        like = Like.objects.get(id=1)
        auto_now = like._meta.get_field('updated_at').auto_now
        self.assertEqual(auto_now, True)

    def test_created_at_editable(self):
        like = Like.objects.get(id=1)
        editable = like._meta.get_field('created_at').editable
        self.assertEqual(editable, False)

    def test_deleted_at_null(self):
        like = Like.objects.get(id=1)
        null = like._meta.get_field('deleted_at').null
        self.assertEqual(null, True)

    def test_deleted_at_blank(self):
        like = Like.objects.get(id=1)
        blank = like._meta.get_field('deleted_at').blank
        self.assertEqual(blank, True)
