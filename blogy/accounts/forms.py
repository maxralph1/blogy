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
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'name', 'phone',
                  'about_me', 'web', 'instagram', 'twitter']

    username = forms.CharField(
        label='Account Username (cannot be changed)*',
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'e.g. abc123',
                   'id': 'username', 'readonly': 'readonly'}
        )
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'e.g. john@doe.com', 'id': 'email'}
        )
    )
    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'e.g. John Doe', 'name': 'name', 'id': 'name'}
        )
    )
    phone = forms.CharField(
        label='Phone',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'e.g. +123456789', 'name': 'phone', 'id': 'phone'}
        ))
    about_me = forms.CharField(
        label='About Me',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'e.g. I am so so and so', 'name': 'about_me', 'id': 'about_me'}
        ))
    web = forms.CharField(
        label='Web Address',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'e.g. http://johndoe.com/', 'name': 'web', 'id': 'web'}
        ))
    instagram = forms.CharField(
        label='Instagram',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'e.g. http://instagram.com/johndoe/', 'name': 'instagram', 'id': 'instagram'}
        ))
    twitter = forms.CharField(
        label='Twitter',
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'e.g. http://twitter.com/johndoe/', 'name': 'twitter', 'id': 'twitter'}
        ))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['email'].required = False
        self.fields['name'].required = False
        self.fields['phone'].required = False
        self.fields['about_me'].required = False
        self.fields['web'].required = False
        self.fields['instagram'].required = False
        self.fields['twitter'].required = False

    def clean_username(self):
        username = self.cleaned_data['username']
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_name(self):
        name = self.cleaned_data['name']
        return name

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        return phone

    def clean_about_me(self):
        about_me = self.cleaned_data['about_me']
        return about_me

    def clean_web(self):
        web = self.cleaned_data['web']
        return web

    def clean_instagram(self):
        instagram = self.cleaned_data['instagram']
        return instagram

    def clean_twitter(self):
        twitter = self.cleaned_data['twitter']
        return twitter


class UserPhotoForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['photo']

    photo = forms.CharField(
        label='Profile Photo*',
        widget=forms.TextInput(
            attrs={'type': 'file', 'class': 'form-control', 'placeholder': 'Update Profile Photo',
                   'id': 'photo'}
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].required = False

    def clean_photo(self):
        photo = self.cleaned_data['photo']
        return photo
