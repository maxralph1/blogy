from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import UserModel


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='Username',
        min_length=4,
        max_length=50,
        help_text='Username is required')
    email = forms.EmailField(
        max_length=100,
        help_text='Email required',
        error_messages={'required': 'Please enter a valid email address for shipping updates.'})
    name = forms.CharField(
        label='Name',
        min_length=1,
        max_length=100,
        help_text='Name is required')
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput)

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'name', 'password', )

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        response = UserModel.objects.filter(username=username)
        if response.count():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another email. This email is already taken.'
            )
        return email

    def clean_name(self):
        name = self.cleaned_data['name']
        return name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'type': 'text', 'name': 'username', 'id': 'username',
                'class': 'form-control', 'placeholder': 'e.g. abc123', 'required': 'required'}
        )
        self.fields['email'].widget.attrs.update(
            {'type': 'email', 'name': 'email', 'id': 'email', 'class': 'form-control',
                'placeholder': 'you@example.com', 'required': 'required'}
        )
        self.fields['name'].widget.attrs.update(
            {'type': 'text', 'name': 'name', 'id': 'name',
                'class': 'form-control', 'placeholder': 'eg. John Doe', 'required': 'required'}
        )
        self.fields['password'].widget.attrs.update(
            {'type': 'password', 'name': 'password', 'id': 'password',
                'class': 'form-control', 'placeholder': '********', 'required': 'required'}
        )
        self.fields['password2'].widget.attrs.update(
            {'type': 'password', 'id': 'password2',
                'class': 'form-control', 'placeholder': '********', 'required': 'required'}
        )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control',
                   'placeholder': 'e.g. abc123', 'id': 'username', 'name': 'username', 'required': 'required'}
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'type': 'password', 'class': 'form-control',
                   'placeholder': '********', 'id': 'password', 'name': 'password', 'required': 'required'}
        ))
    remember_me = forms.BooleanField(required=False)


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=255,
        widget=forms.TextInput(
            attrs={'type': 'email', 'name': 'email', 'id': 'email', 'class': 'form-control',
                   'placeholder': 'you@example.com', 'required': 'required'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        foundUser = UserModel.objects.filter(email=email)
        if not foundUser:
            raise forms.ValidationError(
                'Unfortunately we can not find an account associated with that email address')
        return email


class PasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(
            attrs={'type': 'password', 'id': 'new-password1',
                   'class': 'form-control', 'placeholder': 'New password', 'required': 'required'}))
    new_password2 = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput(
            attrs={'type': 'password', 'id': 'new-password2',
                   'class': 'form-control', 'placeholder': 'Repeat new password', 'required': 'required'}))


class UserEditForm(forms.ModelForm):
    username = forms.CharField(
        label='Account username (cannot be changed)',
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'e.g. abc123',
                   'id': 'username', 'readonly': 'readonly'}
        )
    )
    email = forms.EmailField(
        label='email',
        min_length=2,
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'e.g. john@doe.com', 'id': 'email'}
        ))
    name = forms.CharField(
        label='Name',
        min_length=2,
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'e.g. John Doe', 'name': 'name', 'id': 'name'}
        ))

    class Meta:
        model = UserModel
        fields = ('username', 'email', 'name')

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['name'].required = True
