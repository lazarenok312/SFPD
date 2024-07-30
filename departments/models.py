from django.db import models
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings


def generate_token():
    return get_random_string(length=64)


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Отдел")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'


class Role(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Отдел")
    name = models.CharField(max_length=100, verbose_name="Должность")
    order = models.IntegerField(default=0, verbose_name="Порядок", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('department', 'name')
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = ['department', 'order']


class ImportantNotification(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    message = models.TextField(verbose_name="Содержание")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Важная информация'
        verbose_name_plural = 'Важная информация'


class PoliceAcademyPosition(models.Model):
    POSITION_CHOICES = [
        ('chief', 'Chief of PA'),
        ('dep_chief1', 'Dep.Chief of PA'),
        ('dep_chief2', 'Dep.Chief of PA'),
    ]

    position = models.CharField(max_length=10, choices=POSITION_CHOICES, verbose_name="Должность")
    nickname = models.CharField(max_length=100, verbose_name="Ник")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to='police_academy_photos/', blank=True, null=True, verbose_name="Фото")

    def __str__(self):
        return f"{self.get_position_display()} - {self.nickname}"

    class Meta:
        verbose_name = 'Должность ПА'
        verbose_name_plural = 'Должности ПА'


class CPDPosition(models.Model):
    POSITION_CHOICES = [
        ('chief', 'Chief of CPD'),
        ('dep_chief1', 'Dep.Chief of CPD'),
        ('dep_chief2', 'Dep.Chief of CPD'),
    ]

    position = models.CharField(max_length=10, choices=POSITION_CHOICES, verbose_name="Должность")
    nickname = models.CharField(max_length=100, verbose_name="Ник")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to='cpd_photos/', blank=True, null=True, verbose_name="Фото")

    def __str__(self):
        return f"{self.get_position_display()} - {self.nickname}"

    class Meta:
        verbose_name = 'Должность CPD'
        verbose_name_plural = 'Должности CPD'


class DBPosition(models.Model):
    POSITION_CHOICES = [
        ('head', 'Head of DB'),
        ('dep_head1', 'Dep.Head of DB'),
        ('dep_head2', 'Dep.Head of DB'),
    ]

    position = models.CharField(max_length=10, choices=POSITION_CHOICES, verbose_name="Должность")
    nickname = models.CharField(max_length=100, verbose_name="Ник")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to='db_photos/', blank=True, null=True, verbose_name="Фото")

    def __str__(self):
        return f"{self.get_position_display()} - {self.nickname}"

    class Meta:
        verbose_name = 'Должность DB'
        verbose_name_plural = 'Должности DB'


class SWATPosition(models.Model):
    POSITION_CHOICES = [
        ('commander', 'Сommander of SWAT'),
        ('dep_commander1', 'Dep. Commander of SWAT'),
        ('dep_commander2', 'Dep. Commander of SWAT'),
    ]

    position = models.CharField(max_length=20, choices=POSITION_CHOICES, verbose_name="Должность")
    nickname = models.CharField(max_length=100, verbose_name="Ник")
    description = models.TextField(verbose_name="Описание")
    photo = models.ImageField(upload_to='swat_photos/', blank=True, null=True, verbose_name="Фото")

    def __str__(self):
        return f"{self.get_position_display()} - {self.nickname}"

    class Meta:
        verbose_name = 'Должность SWAT'
        verbose_name_plural = 'Должности SWAT'


class DepartmentStaff(models.Model):
    RANKS = (
        ('sheriff', 'Шериф департамента'),
        ('colonel1', 'Полковник1'),
        ('colonel2', 'Полковник2'),
        ('colonel3', 'Полковник3'),
        ('lcolonel1', 'Подполковник1'),
        ('lcolonel2', 'Подполковник2'),
        ('lcolonel3', 'Подполковник3'),
        ('major1', 'Майор1'),
        ('major2', 'Майор2'),
        ('major3', 'Майор3'),
        ('major4', 'Майор4'),
    )

    name = models.CharField(max_length=100, verbose_name="Имя")
    title = models.CharField(max_length=100, choices=RANKS, verbose_name="Звание")
    photo = models.ImageField(upload_to='department_staff', blank=True, null=True, verbose_name="Фото")
    job_title = models.TextField(max_length=50, blank=True, null=True, verbose_name="Должность")
    discord_url = models.URLField(max_length=200, blank=True, null=True, verbose_name="Ссылка на Discord")
    vk_url = models.URLField(max_length=200, blank=True, null=True, verbose_name="Ссылка на VK")

    def __str__(self):
        return f"{self.name} - {self.get_title_display()}"

    class Meta:
        verbose_name = 'Штаб'
        verbose_name_plural = 'Штаб'


class ContractServiceStatus(models.Model):
    is_active = models.BooleanField(default=False, verbose_name="Статус контракта")

    def notify_subscribers(self):
        if self.is_active:
            subscribers = Subscriber.objects.all()
            for subscriber in subscribers:
                token, created = UnsubscribeToken.objects.get_or_create(email=subscriber.email)
                domain = settings.SITE_DOMAIN if hasattr(settings, 'SITE_DOMAIN') else 'localhost:8000'
                unsubscribe_link = f"https://{domain}/unsubscribe/{token.token}"
                context = {
                    'unsubscribe_link': unsubscribe_link,
                }
                message = render_to_string('emails/contract_service_open.html', context)
                send_mail(
                    'Контрактная служба SFPD открыта',
                    message,
                    'site@sfpd-gov.ru',
                    [subscriber.email],
                    html_message=message,
                )

    def save(self, *args, **kwargs):
        previous_status = ContractServiceStatus.objects.first().is_active if ContractServiceStatus.objects.exists() else None
        super().save(*args, **kwargs)
        if self.is_active and not previous_status:
            self.notify_subscribers()

    def __str__(self):
        return "Статус контракта"

    class Meta:
        verbose_name = 'Статус контракта'
        verbose_name_plural = 'Статус контракта'


class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Электронная почта")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Подписки на рассылку'
        verbose_name_plural = 'Подписки на рассылку'


class UnsubscribeToken(models.Model):
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    token = models.CharField(max_length=64, unique=True, default=generate_token, verbose_name="Токен")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(days=1)

    def __str__(self):
        return f"Токен отписки для {self.email}"

    class Meta:
        verbose_name = 'Токен отписки'
        verbose_name_plural = 'Токен отписки'


class ChangeHistory(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")

    class Meta:
        verbose_name = 'История изменений'
        verbose_name_plural = 'Истории изменений'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
