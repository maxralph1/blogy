from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomAccountsManager(BaseUserManager):
    def validateUsername(self, username):
        try:
            username.isalpha()
        except ValidationError:
            raise ValueError(_('You must provide an alphanumeric username'))

    def validateEmail(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_('You must provide a valid email address'))

    def validatePassword(self, password):
        if len(password) < 8:
            raise ValidationError(
                'This password is too short. It must contain at least 8 characters.',
            )

    def create_superuser(self, username, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be assigned to is_staff=True'))
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                _('Superuser must be assigned to is_superuser=True'))

        return self.create_user(username, email, password, **other_fields)

    def create_user(self, username, email, password, **other_fields):
        user = self.model(username=username, email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('Username'),
        max_length=100,
        unique=True
    )
    email = models.CharField(
        _('Email Address'),
        max_length=150,
        unique=True
    )
    name = models.CharField(
        _('Name'),
        max_length=100
    )
    password = models.CharField(
        _('Password'),
        max_length=50
    )
    phone = models.CharField(
        _('Phone Number'),
        max_length=20,
        null=True,
        blank=True
    )
    photo = models.ImageField(
        verbose_name=_('Blogger photo'),
        help_text=_('Upload image'),
        upload_to='images/bloggers/',
        default='images/default.png',
        null=True,
        blank=True
    )
    about_me = models.TextField(
        _('About me'),
        max_length=100,
        null=True,
        blank=True
    )
    web = models.CharField(
        verbose_name=_('Blogger Website'),
        max_length=255,
        null=True,
        blank=True
    )
    instagram = models.CharField(
        verbose_name=_('Blogger Instagram'),
        max_length=255,
        null=True,
        blank=True
    )
    twitter = models.CharField(
        verbose_name=_('Blogger Twitter'),
        max_length=255,
        null=True,
        blank=True
    )
    remember_me = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = CustomAccountsManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'no-reply@blogy.com',
            [self.email],
            fail_silently=False
        )

    def __str__(self):
        return self.username

    @property
    def photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
