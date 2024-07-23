from django.db import models


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
    name = models.CharField(max_length=100, unique=True, verbose_name="Должность")

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['department', 'name'], name='unique_role_per_department')
        ]
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class ImportantInfo(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Отдел")
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    date_posted = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

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
