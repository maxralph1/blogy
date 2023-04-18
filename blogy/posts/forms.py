from ckeditor_uploader.widgets import CKEditorUploadingWidget

from django import forms
from .models import Topic, Article, Comment, Reaction


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'description']

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        return description

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'type': 'text', 'name': 'title', 'id': 'title',
                'class': 'form-control', 'placeholder': 'Title', 'required': 'required'}
        )
        self.fields['description'].widget.attrs.update(
            {'type': 'text', 'name': 'description', 'id': 'description',
                'class': 'form-control', 'placeholder': 'Describe the topic', 'required': 'required'}
        )


class ArticleForm(forms.ModelForm):
    class Meta:
        content = forms.CharField(widget=CKEditorUploadingWidget())
        model = Article
        fields = ['title', 'body', 'image', 'topic']

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_body(self):
        body = self.cleaned_data['body']
        return body

    def clean_image(self):
        image = self.cleaned_data['image']
        return image

    def clean_topic(self):
        topic = self.cleaned_data['topic']
        return topic

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'type': 'text', 'name': 'title', 'id': 'title',
                'class': 'form-control form-control-line', 'placeholder': 'Title', 'required': 'required'}
        )
        self.fields['body'].widget.attrs.update(
            widget=CKEditorUploadingWidget())

        self.fields['image'].widget.attrs.update(
            {'type': 'file', 'name': 'image', 'id': 'image',
                'class': 'form-control form-control-line', 'placeholder': 'e.g. img/hsg.jpg'}
        )
        self.fields['topic'].widget.attrs.update(
            {'type': 'text', 'name': 'topic', 'id': 'topic',
                'class': 'form-select shadow-none form-control-line', 'placeholder': 'Choose topic'}
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title', 'body']

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_body(self):
        body = self.cleaned_data['body']
        return body

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'type': 'text', 'name': 'title', 'id': 'title',
                'class': 'form-control', 'placeholder': 'Title of comment', 'required': 'required'}
        )
        self.fields['body'].widget.attrs.update(
            {'type': 'text', 'name': 'body', 'id': 'body',
                'class': 'form-control', 'placeholder': 'Write your comment', 'required': 'required'}
        )


class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ['type']

    def clean_type(self):
        type = self.cleaned_data['type']
        return type
