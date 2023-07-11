from django import forms
from .models import Newsletter


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'type': 'email', 'name': 'email', 'id': 'email',
                'class': 'form-control', 'placeholder': 'john@doe.com', 'required': 'required'}
        )
