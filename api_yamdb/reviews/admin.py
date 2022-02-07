from django.contrib import admin
from reviews.models import Review, Comment
from reviews.models import Category, Genre, Title, Genre_Title


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    list_editable = ('text', 'score')
    search_fields = ('text',)
    list_filter = ('pub_date', 'author')
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'pub_date'
    )
    list_editable = ('text',)
    search_fields = ('text', 'author')
    list_filter = ('pub_date', 'author')
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_editable = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_editable = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'year', 'category')
    list_editable = ('name', 'year', 'category')
    search_fields = ('name', 'category', 'genre')
    list_filter = ('year', 'category', 'genre')
    empty_value_display = '-пусто-'


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'genre', 'title')
    list_editable = ('genre', 'title')
    search_fields = ('genre', 'title')
    list_filter = ('genre', 'title')
    empty_value_display = '-пусто-'


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre_Title, GenreTitleAdmin)
