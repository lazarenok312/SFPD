from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Отдел")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'


class Role(models.Model):
    name = models.CharField(max_length=100, verbose_name="Должность")
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.department.name})"

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class ImportantInfo(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)


class PoliceAcademyPosition(models.Model):
    POSITION_CHOICES = [
        ('chief', 'Chief of PA'),
        ('dep_chief1', 'Dep.Chief of PA'),
        ('dep_chief2', 'Dep.Chief of PA'),
    ]

    position = models.CharField(max_length=10, choices=POSITION_CHOICES)
    nickname = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='police_academy_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.get_position_display()} - {self.nickname}"