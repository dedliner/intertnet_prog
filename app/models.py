
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    short_content = models.TextField(max_length=500, verbose_name="Краткое содержание")
    full_content = models.TextField(verbose_name="Полное содержание")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Автор статьи", related_name="articles")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    # НОВОЕ ПОЛЕ: Изображение для статьи
    image = models.ImageField(
        upload_to='article_images/',
        verbose_name="Изображение статьи",
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = "Статья блога"
        verbose_name_plural = "Статьи блога"
        ordering = ['-published_date']
    
    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField(max_length=1000, verbose_name="Текст комментария")
    date = models.DateTimeField(default=timezone.now, verbose_name="Дата добавления")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария", related_name="comments")
    post = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Статья", related_name="comments")
    
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-date']
    
    def __str__(self):
        return f"Комментарий от {self.author.username}"
