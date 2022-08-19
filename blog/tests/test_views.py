from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User # Required to assign User as an author

from blog.models import Author, Blog


class BlogPostListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        test_user = User.objects.create_user(username='test_user', password='1X<ISRUkw+tuK')
        author = Author.objects.create(name=test_user, biography='My biography.')

        # Create 13 posts for pagination tests
        number_of_posts = 8

        for blog_id in range(number_of_posts):
            Blog.objects.create(
                title=f'title {blog_id}',
                content=f'blog #{blog_id}',
                author=author,
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/blogs/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_list.html')

    def test_pagination_is_five(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['blog_list']), 5)

    def test_lists_all_authors(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('blogs')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['blog_list']), 3)
        

class AuthorListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        # Create 13 authors
        number_of_authors = 13

        for author_id in range(number_of_authors):
            test_user = User.objects.create_user(username=f'test_user {author_id}',
                                                 password='1X<ISRUkw+tuK')
            Author.objects.create(
                name=test_user,
                biography=f'Biography #{author_id}',
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/bloggers/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/author_list.html')

    def test_pagination_is_off(self):
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == False)

    def test_lists_all_authors(self):
        # Get author page and confirm it has 13 items
        response = self.client.get(reverse('authors'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['author_list']), 13)  

class CommentFormViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        testuser1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        testuser2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        author1 = Author.objects.create(name=testuser1, biography='My biography.')
        author2 = Author.objects.create(name=testuser2, biography='My biography.')

        Blog.objects.create(title='title', content='blog content', author=author1, post_date=timezone.now())

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('create-comment', kwargs={'pk': 1}))
        self.assertRedirects(response, '/accounts/login/?next=/blog/blogs/1/create')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='2HJ1vRV0Z&3iD')
        response = self.client.get(reverse('create-comment', kwargs={'pk': 1}))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser2')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)

        # Check we used correct template
        self.assertTemplateUsed(response, 'blog/create_comment.html')
 