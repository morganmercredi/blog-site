from django.db import models    
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User

class Blog(models.Model):
    """Model representing a blog post."""
    # Title of the post
    title = models.CharField(max_length=200)

    # Foreign Key used because a post can only have one author, but authors can have multiple posts
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    # The content of the blog post
    content = models.TextField(max_length=5000, help_text='Write your blog post here.')
    
    # The date the blog was posted
    post_date = models.DateField(null=True)
    
    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this post."""
        return reverse('blog-detail', args=[str(self.id)])    
    
class Author(models.Model):
    """Model representing an author."""
    # The User attached to this author
    name = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    
    # A brief biography of the author
    biography = models.TextField(max_length=1000)
    
    def get_absolute_url(self):
        """Returns the URL to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'
    
class Comment(models.Model):
    """Model representing a specific comment on a blog post."""
    # A foreign key for the blog post for this comment
    blog = models.ForeignKey('Blog', on_delete=models.RESTRICT, null=True)
    
    # The comment content
    content = models.TextField(max_length=200)
    
    # The time the comment was posted
    post_date = models.DateTimeField(null=True)
    
    # Foreign Key used because a comment can only have one author (user), but authors (users) can have multiple comments
    # Author as a string rather than object because it hasn't been declared yet in the file    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['post_date']
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.blog.title})'

    def display_comment(self):
        """Create a shortened string to display on Admin site."""
        return self.content[:50]
    
    display_comment.short_description = 'Comment (truncated)'
