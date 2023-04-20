from ckeditor.fields import RichTextField

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from accounts.models import UserModel


class Topic(models.Model):
    title = models.CharField(
        verbose_name=_('Topic Title'),
        help_text=_('Required and unique'),
        max_length=30,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_(
            'Topic safe URL'),
        max_length=255,
        unique=True)
    description = models.CharField(
        verbose_name=_('Topic Description'),
        help_text=_('Required and unique'),
        max_length=255,
    )
    representative_color = models.CharField(
        max_length=10,
        default='secondary'
    )
    added_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        verbose_name=_('Topic visibility'),
        help_text=_('Change topic visibility'),
        default=True,
    )
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

    def get_absolute_url(self):
        return reverse('posts:topics', args=[self.slug])

    def __str__(self):
        return self.title


class Article(models.Model):
    is_featured = models.BooleanField(
        verbose_name=_('Make article Featured'),
        help_text=_('Change make article featured on index(home) page'),
        default=False,
    )
    title = models.CharField(
        verbose_name=_('Article Title'),
        help_text=_('Required, unique and 20 charcters maximum'),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_(
            'Article safe URL'),
        max_length=255,
        unique=True)
    body = RichTextField(
        verbose_name=_('Write your Article'),
        unique=True,
    )
    image = models.ImageField(
        verbose_name=_('Article Preview Image'),
        help_text=_('Upload image image'),
        upload_to='images/articles/',
        default='images/default.png',
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        verbose_name=_('Choose a Topic'
                       ))
    added_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        verbose_name=_('Topic visibility'),
        help_text=_('Change topic visibility'),
        default=True,
    )
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    def get_absolute_url(self):
        return reverse('posts:articles', args=[self.slug])

    def __str__(self):
        return self.title

    # def commented_on_recently(self):
    #     # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    #     self.comment.created_at
    #     now = timezone.now()
    #     return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Comment(models.Model):
    title = models.CharField(
        verbose_name=_('Comment Title'),
        help_text=_('Required and unique'),
        max_length=255
    )
    slug = models.SlugField(
        verbose_name=_(
            'Comment safe URL'),
        max_length=255,
        unique=True)
    body = models.TextField(
        verbose_name=_('Body'),
        max_length=255
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    added_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        verbose_name=_('Comment visibility'),
        help_text=_('Change comment visibility'),
        default=True,
    )
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)


class Reaction(models.Model):
    REACTION_CHOICES = [
        ('LIKE', '👍'),
        ('LOVE', '😍'),
        ('LAUGH', '😂'),
        ('SURPRISED', '😮'),
        ('ANGRY', '😡'),
        ('SAD', '😢'),
    ]

    type = models.CharField(
        choices=REACTION_CHOICES,
        verbose_name=_('Reaction Choices'),
        help_text=_('Required'),
        max_length=255,
        null=True,
        blank=True
    )
    slug = models.SlugField(
        verbose_name=_(
            'Reaction safe URL'),
        max_length=255,
        unique=True
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    added_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        verbose_name=_('Reaction visibility'),
        help_text=_('Change reaction visibility'),
        default=True,
    )
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
