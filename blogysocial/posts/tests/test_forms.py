from django.test import TestCase

from posts.forms import TopicForm, ArticleForm, CommentForm


class TopicFormTest(TestCase):
    def test_topic_form_title_field_help_text(self):
        form = TopicForm()
        self.assertTrue(
            form.fields['title'].help_text == 'Required and unique'
        )

    def test_topic_form_title_field_cleaned_data(self):
        title_input = str('title')
        form = TopicForm(data={'title': title_input})
        self.assertFalse(form.is_valid())

    def test_topic_form_description_field_cleaned_data(self):
        description_input = str('description')
        form = TopicForm(data={'description': description_input})
        self.assertFalse(form.is_valid())


class ArticleFormTest(TestCase):
    def test_article_form_title_field_help_text(self):
        form = ArticleForm()
        self.assertTrue(
            form.fields['title'].help_text == 'Required and unique'
        )

    def test_article_form_title_field_cleaned_data(self):
        title_input = str('title')
        form = ArticleForm(data={'title': title_input})
        self.assertFalse(form.is_valid())

    def test_article_form_body_field_cleaned_data(self):
        body_input = str('body')
        form = ArticleForm(data={'body': body_input})
        self.assertFalse(form.is_valid())

    def test_article_form_image_field_cleaned_data(self):
        image_input = str('image')
        form = ArticleForm(data={'image': image_input})
        self.assertFalse(form.is_valid())

    def test_article_form_topic_field_cleaned_data(self):
        topic_input = str('topic')
        form = ArticleForm(data={'topic': topic_input})
        self.assertFalse(form.is_valid())


class CommentFormTest(TestCase):
    def test_comment_form_title_field_help_text(self):
        form = CommentForm()
        self.assertTrue(
            form.fields['title'].help_text == 'Comment Title'
        )

    def test_comment_form_title_field_cleaned_data(self):
        title_input = str('title')
        form = CommentForm(data={'title': title_input})
        self.assertFalse(form.is_valid())

    def test_comment_form_body_field_cleaned_data(self):
        body_input = str('body')
        form = CommentForm(data={'body': body_input})
        self.assertFalse(form.is_valid())
