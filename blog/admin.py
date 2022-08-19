from django.contrib import admin

from .models import Author, Blog, Comment

admin.site.register(Author)

   
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

# Register the Admin class for Blog using the decorator
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'post_date')
    search_fields = ['title']
    list_filter = ['post_date']
    inlines = [CommentInline]
    
@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ('author', 'post_date', 'display_comment')    
