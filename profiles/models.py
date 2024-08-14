from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from departments.models import Role, Department
from django.utils.crypto import get_random_string
from django.utils.text import slugify


class RegRole(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фракция'
        verbose_name_plural = 'Фракция'


class Badge(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название значка")
    image = models.ImageField(upload_to='badges/', verbose_name="Изображение значка")
    description = models.TextField(verbose_name="Описание значка", blank=True)
    priority = models.IntegerField(default=0, verbose_name="Приоритет")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Значок'
        verbose_name_plural = 'Значки'
        ordering = ['-priority']


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    reg_role = models.ForeignKey(RegRole, verbose_name="Фракция", on_delete=models.SET_NULL, null=True, blank=True,
                                 default=None)
    name = models.CharField(max_length=25, verbose_name="Имя", blank=True)
    surnames = models.CharField(max_length=25, verbose_name="Фамилия", blank=True)
    email = models.EmailField(max_length=40, verbose_name="Электронная почта", blank=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, verbose_name="Фото",
                              default='../static/images/incognito.png')
    slug = models.SlugField("URL", max_length=50, blank=True, unique=True)
    last_activity = models.DateTimeField(verbose_name="Последняя активность", default=timezone.now)
    bio = models.TextField(verbose_name="Биография", blank=True)
    department = models.ForeignKey(Department, verbose_name="Отдел", on_delete=models.CASCADE, blank=True, null=True)
    role = models.ForeignKey(Role, verbose_name="Должность", on_delete=models.CASCADE, blank=True, null=True)
    nick_name = models.CharField(max_length=50, verbose_name="Игровой ник", blank=True)
    profile_confirmed = models.BooleanField(default=False, verbose_name="Подтверждение профиля")
    role_confirmed = models.BooleanField(default=False, verbose_name="Подтверждение должности")
    likes = models.PositiveIntegerField(default=0, verbose_name="Лайки")
    dislikes = models.PositiveIntegerField(default=0, verbose_name="Дизлайки")
    birthdate = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    last_viewed_news = models.DateTimeField(null=True, blank=True, verbose_name="Последнее посещение новостей")
    last_viewed_changes = models.DateTimeField(null=True, blank=True,
                                               verbose_name="Последнее посещение истории изменений")
    badges = models.ManyToManyField(Badge, blank=True, related_name="profiles", verbose_name="Значки")
    rating = models.PositiveIntegerField(default=0, verbose_name="Рейтинг")
    level = models.PositiveIntegerField(default=1, verbose_name="Уровень")

    def update_rating(self, points):
        self.rating += points
        if self.rating >= self.get_next_level_threshold():
            self.level_up()
        self.save()

    def level_up(self):
        self.level += 1
        self.rating = 0

    def get_next_level_threshold(self):
        return self.level * 100

    def reset_rating(self):
        self.rating = 0
        self.save()

    @property
    def status(self):
        return "Администратор" if self.user.is_staff else "Пользователь"

    def is_editor(self):
        return self.user.groups.filter(name="Редактор").exists()

    @property
    def is_online(self):
        now = timezone.now()
        return now - self.last_activity < timezone.timedelta(minutes=2)

    def __str__(self):
        return 'Профиль пользователя {}'.format(self.user.username)

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.pk:
            original = Profile.objects.get(pk=self.pk)
            if original.role != self.role:
                self.role_confirmed = False

        if not self.slug:
            self.slug = slugify(self.user.username)

        super().save(*args, **kwargs)

    @classmethod
    def get_birthdays_in_month(cls, month, year):
        return cls.objects.filter(birthdate__month=month, birthdate__year=year)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class ActivityLog(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Профиль")
    activity_type = models.CharField(max_length=50, verbose_name="Тип активности")
    points = models.PositiveIntegerField(default=0, verbose_name="Очки за активность")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.profile.update_rating(self.points)

    class Meta:
        verbose_name = 'Лог активности'
        verbose_name_plural = 'Логи активности'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            email=instance.email,
            name=instance.first_name,
            surnames=instance.last_name
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    profile = instance.profile
    profile.name = instance.first_name
    profile.surnames = instance.last_name
    profile.email = instance.email
    profile.save()


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
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    change_type = models.CharField(max_length=255, verbose_name="Тип изменения")
    old_value = models.TextField(blank=True, verbose_name="Старое значение")
    new_value = models.TextField(blank=True, verbose_name="Новое значение")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время")

    def __str__(self):
        return f"{self.user} {self.change_type} с {self.old_value} на {self.new_value}"

    class Meta:
        verbose_name = 'Логи изменений'
        verbose_name_plural = 'Логи изменений'


class LikeDislike(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, verbose_name="Профиль", on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True, verbose_name="Лайк")

    class Meta:
        unique_together = ('user', 'profile')
        verbose_name = 'Лайк/Дизлайк'
        verbose_name_plural = 'Лайки/Дизлайки'


class ProfileConfirmationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation_token')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_token(self):
        self.token = get_random_string(64)
        self.save()

    def is_expired(self):
        return self.created_at < timezone.now() - timezone.timedelta(hours=24)

    class Meta:
        verbose_name = 'Токен подтверждения'
        verbose_name_plural = 'Токены подтверждения'


class EmailLog(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Email to {self.recipient} at {self.sent_at}"

    class Meta:
        verbose_name = 'Логи Email'
        verbose_name_plural = 'Логи Email'
