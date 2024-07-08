from django.db import models
from django.contrib.auth import get_user_model
from django.apps import apps

User = get_user_model()

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE)
    role = models.ForeignKey('departments.Role', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Профиль сотрудника'
        verbose_name_plural = 'Профили сотрудников'

    def __str__(self):
        return f"{self.user.username} ({self.department.name}) - {self.role.name}"