from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

CROP_TEXT: int = 15


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Наименование группы')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='URL-группы')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст поста')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор')
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Сообщество')
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='posts/',
        blank=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:CROP_TEXT]
