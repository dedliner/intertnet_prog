from django.contrib import admin
from .models import Article, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'short_content', 'published_date', 'created_date')
    list_filter = ('published_date', 'created_date', 'author')
    search_fields = ('title', 'short_content', 'full_content', 'author__username')
    list_editable = ('short_content',)
    list_per_page = 10
    ordering = ('-published_date',)
    readonly_fields = ('created_date', 'updated_date')


class CommentAdmin(admin.ModelAdmin):
    """Настройка отображения комментариев в админке"""
    list_display = ('text_preview', 'author', 'post', 'date')
    list_filter = ('date', 'author', 'post')
    search_fields = ('text', 'author__username', 'post__title')
    list_per_page = 20
    ordering = ('-date',)
    readonly_fields = ('date',)
    
    def text_preview(self, obj):
        """Показывает первые 50 символов комментария"""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = "Текст комментария"


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)