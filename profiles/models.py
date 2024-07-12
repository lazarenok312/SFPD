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
