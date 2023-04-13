from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Newsletter(models.Model):
    email = models.CharField(
        _('Email Address'),
        max_length=150,
        unique=True)
    is_active = models.BooleanField(
        verbose_name=_('Newsletter visibility'),
        help_text=_('Change newsletter visibility'),
        default=True,
    )
    created_at = models.DateTimeField(
        _('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Newsletter')
        verbose_name_plural = _('Newsletters')

    def get_absolute_url(self):
        return reverse('posts:newsletters', args=[self.slug])

    def __str__(self):
        return self.title
