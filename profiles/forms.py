from django import forms
from django.contrib.auth.models import User
from profiles.models import Profile
from .models import SupportRequest
from departments.models import Department, Role


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd.get('password2'):
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует.')
        return username


class ProfileUpdateForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='Выберите отдел',
                                        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_department'}))
    role = forms.ModelChoiceField(queryset=Role.objects.none(), empty_label='Выберите должность',
                                  widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_role'}))

    class Meta:
        model = Profile
        fields = ['name', 'surnames', 'email', 'photo', 'bio', 'department', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surnames': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'department': forms.Select(attrs={'class': 'form-control', 'id': 'id_department'}),
            'role': forms.Select(attrs={'class': 'form-control', 'id': 'id_role'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.department:
            self.fields['role'].queryset = Role.objects.filter(department=self.instance.department)
        self.fields['department'].widget.attrs.update({'onchange': 'loadRoles()'})


class SupportForm(forms.ModelForm):
    class Meta:
        model = SupportRequest
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш email',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше сообщение',
                'rows': 4,
                'required': True
            }),
        }
