from django.test import TestCase

from blog.forms import CommentForm

class CommentFormTest(TestCase):
    def test_comment_form_label(self):
        form = CommentForm()
        self.assertTrue(form.fields['content'].label is None or form.fields['content'].label == 'Comment')

    def test_comment_form_help_text(self):
        form = CommentForm()
        self.assertEqual(form.fields['content'].help_text, 'Enter a comment')

    def test_comment_form_max_length(self):
        form = CommentForm()
        self.assertEqual(form.fields['content'].max_length, 200)

