from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

class Role(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.department.name})"

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'


class ImportantInfo(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

class PersonalFile(models.Model):
    employee = models.OneToOneField('profiles.EmployeeProfile', on_delete=models.CASCADE)
    details = models.TextField()

class HonorsBoard(models.Model):
    employee = models.ForeignKey('profiles.EmployeeProfile', on_delete=models.CASCADE)
    description = models.TextField()
    date_awarded = models.DateTimeField(auto_now_add=True)