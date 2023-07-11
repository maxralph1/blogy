from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse

from .forms import NewsletterForm
from .models import Newsletter


def subcribe_to_newsletter(request):
    if request.method == 'POST':
        newsletter_form = NewsletterForm(request.POST)

        if newsletter_form.is_valid():
            newsletter = newsletter_form.save(commit=False)
            newsletter.title = newsletter_form.cleaned_data['email']
            newsletter.save()

            messages.success(request, 'You have subscribed to our newsletters')

        else:
            return HttpResponse('Error', status=400)

    else:
        newsletter_form = NewsletterForm()
