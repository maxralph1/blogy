from django import forms
from .models import Category, Article, Comment, Reaction


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
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
                'class': 'form-control', 'placeholder': 'Describe the category', 'required': 'required'}
        )


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'image', 'category']

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_body(self):
        body = self.cleaned_data['body']
        return body

    def clean_image(self):
        image = self.cleaned_data['image']
        return image

    def clean_category(self):
        category = self.cleaned_data['category']
        return category

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update(
            {'type': 'text', 'name': 'title', 'id': 'title',
                'class': 'form-control', 'placeholder': 'Title', 'required': 'required'}
        )
        self.fields['body'].widget.attrs.update(
            {'type': 'text', 'name': 'body', 'id': 'body',
                'class': 'form-control', 'placeholder': 'Write your article', 'required': 'required'}
        )
        self.fields['image'].widget.attrs.update(
            {'type': 'file', 'name': 'image', 'id': 'image',
                'class': 'form-control', 'placeholder': 'e.g. img/hsg.jpg'}
        )
        self.fields['category'].widget.attrs.update(
            {'type': 'text', 'name': 'category', 'id': 'category',
                'class': 'form-select', 'placeholder': 'Choose category', 'required': 'required'}
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
