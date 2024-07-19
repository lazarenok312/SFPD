from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from departments.models import Role, Department


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    name = models.CharField(max_length=25, verbose_name="Имя", blank=True)
    surnames = models.CharField(max_length=25, verbose_name="Фамилия", blank=True)
    email = models.EmailField(max_length=40, verbose_name="Электронная почта", blank=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, verbose_name="Фото",
                              default='../static/img/default.png')
    slug = models.SlugField("URL", max_length=50, blank=True)
    last_activity = models.DateTimeField(verbose_name="Последняя активность", default=timezone.now)
    bio = models.TextField(verbose_name="Биография", blank=True)
    department = models.ForeignKey(Department, verbose_name="Отдел", on_delete=models.CASCADE, blank=True, null=True)
    role = models.ForeignKey(Role, verbose_name="Должность", on_delete=models.CASCADE, blank=True, null=True)
    nick_name = models.CharField(max_length=50, verbose_name="Игровой ник", blank=True)
    profile_confirmed = models.BooleanField(default=False, verbose_name="Подтверждение профиля")
    role_confirmed = models.BooleanField(default=False, verbose_name="Подтверждение должности")
    likes = models.PositiveIntegerField(default=0, verbose_name="Лайки")
    dislikes = models.PositiveIntegerField(default=0, verbose_name="Дизлайки")

    @property
    def status(self):
        return "Администратор" if self.user.is_staff else "Пользователь"

    @property
    def is_online(self):
        now = timezone.now()
        return now - self.last_activity < timezone.timedelta(minutes=2)

    def __str__(self):
        return 'Профиль пользователя {}'.format(self.user.username)

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = "{}".format(self.user.username)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиля'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class SupportRequest(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ваше имя', blank=True)
    email = models.EmailField(verbose_name='Электронная почта')
    message = models.TextField(verbose_name='Текст обращения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f"Обращение от {self.email} ({self.created_at})"

    class Meta:
        verbose_name = 'Обращение в поддержку'
        verbose_name_plural = 'Обращения в поддержку'


class ProfileChangeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    change_type = models.CharField(max_length=255)
    old_value = models.TextField(blank=True)
    new_value = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.change_type} from {self.old_value} to {self.new_value}"

    class Meta:
        verbose_name = 'Логи изменений'
        verbose_name_plural = 'Логи изменений'


class LikeDislike(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, verbose_name="Профиль", on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True, verbose_name="Лайк")

    class Meta:
        unique_together = ('user', 'profile')

    class Meta:
        verbose_name = 'Лайки Дизлайки'
        verbose_name_plural = 'Лайки Дизлайки'
