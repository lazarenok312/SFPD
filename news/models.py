from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class NewsImage(models.Model):
    image = models.ImageField(upload_to='preloaded_images/', verbose_name="Изображение")
    description = models.CharField(max_length=200, verbose_name="Описание", blank=True, null=True)

    def __str__(self):
        return self.description or "Без описания"

    class Meta:
        verbose_name = 'Загруженное изображение'
        verbose_name_plural = 'Загруженные изображения'


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = RichTextField(verbose_name="Описание")
    image = models.ForeignKey(NewsImage, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Изображение")
    created_at = models.DateTimeField(verbose_name="Дата создания")
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    is_pinned = models.BooleanField(default=False, verbose_name="Закреплено")

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes_dislikes.filter(vote=LikeDislike.LIKE).count()

    def total_dislikes(self):
        return self.likes_dislikes.filter(vote=LikeDislike.DISLIKE).count()

    def total_comments(self):
        return self.comments.count()

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class LikeDislike(models.Model):
    LIKE = 1
    DISLIKE = -1
    VOTE_CHOICES = (
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь",
                             related_name='news_likes_dislikes')
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name="Новость", related_name="likes_dislikes")
    vote = models.SmallIntegerField(choices=VOTE_CHOICES, verbose_name="Голос")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f'{self.user.username} - {self.get_vote_display()}'

    class Meta:
        unique_together = ('user', 'news')
        verbose_name = 'Лайк/Дизлайк'
        verbose_name_plural = 'Лайки/Дизлайки'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments", verbose_name="Новость")
    content = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f'Комментарий от {self.user.username} на {self.news.title}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
