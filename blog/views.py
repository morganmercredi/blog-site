from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required

from .models import Blog, Author, Comment
from blog.forms import CommentForm
import datetime

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_posts = Blog.objects.all().count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()
    
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1    

    context = {
        'num_posts': num_posts,
        'num_authors': num_authors,
        'num_visits': num_visits
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'blog/index.html', context=context)

class BlogListView(generic.ListView):
    model = Blog
    context_object_name  = 'blog_list'
    paginate_by = 5
    template_name = 'blog/blog_list.html'
        
class BlogDetailView(generic.DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'  
    
class AuthorListView(generic.ListView):
    model = Author
    template_name = 'blog/author_list.html'
        
class AuthorDetailView(generic.DetailView):
    model = Author   
    template_name = 'blog/author_detail.html'
    paginate_by=1
        
class BlogListByAuthorView(generic.ListView):
    """
    Generic class-based view for a list of blogs posted by a particular Author.
    """
    model = Blog
    context_object_name = 'blog_list'
    paginate_by = 5
    template_name ='blog/blog_list_by_author.html'
    
    def get_queryset(self):
        """
        Return list of Blog objects created by Author (author id specified in URL)
        """
        id = self.kwargs['pk']
        target_author=get_object_or_404(Author, pk=id)
        return Blog.objects.filter(author=target_author)
        
    def get_context_data(self, **kwargs):
        """
        Add Author to context so they can be displayed in the template
        """
        # Call the base implementation first to get a context
        context = super(BlogListByAuthorView, self).get_context_data(**kwargs)
        # Get the blogger object from the "pk" URL parameter and add it to the context
        context['author'] = get_object_or_404(Author, pk = self.kwargs['pk'])
        return context

@login_required    
def create_comment(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = CommentForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # Use the data in form.cleaned_data to create a new comment and save it
            comment_author = request.user
            content = form.cleaned_data['content']
            comment = Comment.objects.create(content=content,
                                             blog=blog,
                                             author=comment_author,
                                             post_date=timezone.now())
            comment.save()

            # Redirect to a new URL:
            return HttpResponseRedirect(reverse('blog-detail', kwargs={'pk': pk}))

    # If this is a GET (or any other method) create the default form.
    else:
        form = CommentForm()

    context = {
        'form': form,
        'blog': blog,
    }

    return render(request, 'blog/create_comment.html', context)  
