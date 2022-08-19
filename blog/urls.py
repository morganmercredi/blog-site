from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bloggers/', views.AuthorListView.as_view(), name='authors'),
    path('bloggers/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('bloggers2/<int:pk>', views.BlogListByAuthorView.as_view(), name='blogs-by-author'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('blogs/<int:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('blogs/<int:pk>/create', views.create_comment, name='create-comment')
]