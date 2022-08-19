from django.test import TestCase
from django.contrib.auth.models import User

from blog.models import Author, Blog, Comment
        
class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_user(username='test_user', password='1X<ISRUkw+tuK')
        Author.objects.create(name=test_user, biography='My biography.')

    def test_biography_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('biography').max_length
        self.assertEqual(max_length, 1000)

    def test_object_name_is_author_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = author.name
        self.assertEqual(str(author), str(expected_object_name))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), '/blog/bloggers/1')
        

class BlogModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_user(username='test_user', password='1X<ISRUkw+tuK')
        author = Author.objects.create(name=test_user, biography='My biography.')
        Blog.objects.create(title='My blog post', content='This is a post.', author=author)

    def test_title_max_length(self):
        blog = Blog.objects.get(id=1)
        max_length = blog._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)
        
    def test_content_max_length(self):
        blog = Blog.objects.get(id=1)
        max_length = blog._meta.get_field('content').max_length
        self.assertEqual(max_length, 5000)        

    def test_object_name_is_title(self):
        blog = Blog.objects.get(id=1)
        expected_object_name = blog.title
        self.assertEqual(str(blog), expected_object_name)

    def test_get_absolute_url(self):
        blog = Blog.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(blog.get_absolute_url(), '/blog/blogs/1')        

        
class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_user(username='test_user', password='1X<ISRUkw+tuK')
        author = Author.objects.create(name=test_user, biography='My biography.')
        blog = Blog.objects.create(title='My blog post', content='This is a post.', author=author)
        Comment.objects.create(content='My comment', blog=blog, author=test_user)

    def test_comment_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('content').max_length
        self.assertEqual(max_length, 200)        


