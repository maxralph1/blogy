from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from accounts.models import UserModel


class Category(models.Model):
    title = models.CharField(
        verbose_name=_('Category Title'),
        help_text=_('Required and unique'),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_(
            'Category safe URL'),
        max_length=255,
        unique=True)
    description = models.CharField(
        verbose_name=_('Category Description'),
        help_text=_('Required and unique'),
        max_length=255,
    )
    added_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        verbose_name=_('Category visibility'),
        help_text=_('Change category visibility'),
        default=True,
    )
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def get_absolute_url(self):
        return reverse('posts:categories', args=[self.slug])

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(
        verbose_name=_('Article Title'),
        help_text=_('Required and unique'),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_(
            'Article safe URL'),
        max_length=255,
        unique=True)
    body = models.TextField(
        verbose_name=_('Body'),
        unique=True,
    )
    image = models.ImageField(
        verbose_name=_('Article Image'),
        help_text=_('Upload image image'),
        upload_to='images/articles/',
        default='images/default.png',
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    added_by = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_active = models.BooleanField(
        verbose_name=_('Category visibility'),
        help_text=_('Change category visibility'),
        default=True,
    )
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def get_absolute_url(self):
        return reverse('posts:categories', args=[self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    title = models.CharField(
        verbose_name=_('Comment Title'),
        help_text=_('Required and unique'),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name=_(
            'Comment safe URL'),
        max_length=255,
        unique=True)
    body = models.TextField(
        verbose_name=_('Body'),
        max_length=255,
        unique=True,
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
