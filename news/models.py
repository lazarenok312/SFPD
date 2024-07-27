from django.db import models


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
    description = models.TextField(verbose_name="Описание")
    image = models.ForeignKey(NewsImage, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_pinned = models.BooleanField(default=False, verbose_name="Закреплено")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новости департамента'
        verbose_name_plural = 'Новости департамента'
