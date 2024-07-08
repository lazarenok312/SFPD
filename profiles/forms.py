from django import forms
from django.contrib.auth.models import User
from profiles.models import EmployeeProfile
from departments.models import Department, Role

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class EmployeeProfileForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    role = forms.ModelChoiceField(queryset=Role.objects.none())

    class Meta:
        model = EmployeeProfile
        fields = ['department', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['role'].queryset = Role.objects.filter(department_id=department_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['role'].queryset = self.instance.department.role_set.order_by('name')