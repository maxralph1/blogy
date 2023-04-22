from datetime import datetime

from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from posts.models import Article, Comment
from .forms import UserRegistrationForm, UserLoginForm, CustomPasswordResetForm, UserEditForm, UserPhotoForm
from .models import UserModel
from .tokens import account_activation_token, password_reset_token


def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.username = register_form.cleaned_data['username']
            user.email = register_form.cleaned_data['email']
            user.name = register_form.cleaned_data['name']
            user.set_password(register_form.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = _('Activate your Account')
            message = render_to_string(
                'accounts/registration/account_activation_email.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return render(request, 'accounts/registration/register_email_confirm.html', {'register_form': register_form})
        else:
            return render(request, 'accounts/registration/register.html', {'register_form': register_form})
    else:
        register_form = UserRegistrationForm()
    return render(request, 'accounts/registration/register.html', {'register_form': register_form})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('accounts:dashboard')
    else:
        return render(request, 'accounts/registration/activation_invalid.html')


class UpdatedLoginView(LoginView):
    form_class = UserLoginForm

    def form_valid(self, form):

        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(UpdatedLoginView, self).form_valid(form)


def password_reset(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        passwordResetForm = CustomPasswordResetForm(request.POST)
        if passwordResetForm.is_valid():
            resetEmail = passwordResetForm.cleaned_data['email']
            user = UserModel.objects.get(email=resetEmail)
            current_site = get_current_site(request)
            subject = _('Activate your Account')
            message = render_to_string(
                'accounts/password_reset/password_reset_email.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': password_reset_token.make_token(user),
                },
            )
            user.email_user(subject=subject, message=message)
            return render(request, 'accounts/password_reset/reset_status.html', {'form': passwordResetForm})
        else:
            return render(request, 'accounts/password_reset/password_reset_form.html', {'form': passwordResetForm})
    else:
        passwordResetForm = CustomPasswordResetForm()
    return render(request, 'accounts/password_reset/password_reset_form.html', {'form': passwordResetForm})


@login_required
def dashboard(request):
    articles = Article.objects.filter(
        is_active=True).order_by('-updated_at')[:10]

    my_articles = Article.objects.filter(
        added_by=request.user, is_active=True).order_by('-updated_at')[:10]

    comments_by_me = Comment.objects.filter(
        added_by=request.user, is_active=True).order_by('-updated_at')[:4]

    comments_by_others_on_my_articles = Comment.objects.filter(
        article__added_by=request.user, is_active=True).order_by('-updated_at')[:4]

    return render(request, 'accounts/dashboard/index.html', {
        'articles': articles,
        'my_articles': my_articles,
        'comments_by_me': comments_by_me,
        'comments_by_others_on_my_articles': comments_by_others_on_my_articles
    })


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        userphoto_form = UserPhotoForm(
            instance=request.user, data=request.FILES, files=request.FILES)

        if user_form.is_valid():
            user_form.save()

            return HttpResponseRedirect(reverse('accounts:profile'))
    else:
        user_form = UserEditForm(instance=request.user)
        userphoto_form = UserPhotoForm(instance=request.user)

    return render(request, 'accounts/users/profile.html', {
        'user_form': user_form,
        'userphoto_form': userphoto_form
    })


@login_required
def profile_photo(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        userphoto_form = UserPhotoForm(
            instance=request.user, data=request.POST, files=request.FILES)

        if userphoto_form.is_valid():
            userphoto_form.save()

            return HttpResponseRedirect(reverse('accounts:profile'))
    else:
        user_form = UserEditForm(instance=request.user)
        userphoto_form = UserPhotoForm(instance=request.user)

    return render(request, 'accounts/users/profile.html', {
        'user_form': user_form,
        'userphoto_form': userphoto_form
    })


@login_required
def delete_user(request):
    user = UserModel.objects.get(username=request.user)
    user.is_active = False
    user.deleted_at = datetime.now()
    user.save()
    logout(request)
    return redirect('accounts:delete_confirmation')
