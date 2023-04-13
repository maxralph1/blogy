from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect,  render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _

from .forms import UserRegistrationForm, CustomPasswordResetForm, UserEditForm
from .models import UserModel
from .tokens import account_activation_token, password_reset_token


@login_required
def dashboard(request):

    return render(request, 'accounts/dashboard/index.html', {})


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'accounts/users/edit.html', {'user_form': user_form})


@login_required
def delete_user(request):
    user = UserModel.objects.get(user_name=request.user)
    user.is_active = False
    user.deleted_at = datetime.now()
    user.save()
    logout(request)
    return redirect('accounts:delete_confirmation')


def account_register(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        registerForm = UserRegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.first_name = registerForm.cleaned_data['first_name']
            user.last_name = registerForm.cleaned_data['last_name']
            user.username = registerForm.cleaned_data['username']
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
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
            return render(request, 'accounts/registration/register_email_confirm.html', {'form': registerForm})
        else:
            return render(request, 'accounts/registration/register.html', {'form': registerForm})
    else:
        registerForm = UserRegistrationForm()
    return render(request, 'accounts/registration/register.html', {'form': registerForm})


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


def password_reset_token_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and password_reset_token.check_token(user, token):
        # user.is_active = True
        # user.save()
        # login(request, user)
        # return redirect('accounts:dashboard')
        return render(request, 'accounts/password_reset/password_reset_form.html', {'user': uid})
    else:
        return render(request, 'accounts/registration/activation_invalid.html')


def password_edit(request, user):
    if request.method == 'POST':
        user = UserModel.objects.get(pk=id, user=request.user)
        user_form = UserRegistrationForm(instance=user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('accounts:users'))
    else:
        user = UserModel.objects.get(pk=id, user=request.user)
        user_form = UserRegistrationForm(instance=user)
    return render(request, 'accounts/dashboard/edit_users.html', {'form': user_form})
