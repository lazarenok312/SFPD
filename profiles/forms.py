from django import forms
from django.contrib.auth.models import User
from profiles.models import Profile
from .models import SupportRequest
from departments.models import Department, Role
from profiles.models import RegRole
from .models import InvestigationRequest


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    reg_role = forms.ModelChoiceField(queryset=RegRole.objects.all(), required=True, label="Выберите фракцию")

    class Meta:
        model = User
        fields = ('username', 'reg_role', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd.get('password2'):
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким логином уже существует")
        return username


class ProfileUpdateForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        required=False,
        queryset=Department.objects.exclude(name="Staff SFPD"),
        empty_label='Выберите отдел',
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_department'}),
        label='Отдел'
    )
    role = forms.ModelChoiceField(
        required=False,
        queryset=Role.objects.none(),
        empty_label='Выберите должность',
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_role'}),
        label='Должность'
    )
    photo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        label='Фотография'
    )
    nick_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Игровой никнейм'
    )
    birthdate = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        label='Дата рождения'
    )

    class Meta:
        model = Profile
        fields = ['name', 'surnames', 'email', 'photo', 'bio', 'department', 'role', 'nick_name', 'birthdate']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surnames': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            'birthdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'name': 'Имя',
            'surnames': 'Фамилия',
            'email': 'Электронная почта',
            'bio': 'Биография',
            'birthdate': 'Дата рождения',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].queryset = Role.objects.none()

        if 'department' in self.data:
            try:
                department_id = int(self.data.get('department'))
                self.fields['role'].queryset = Role.objects.filter(department_id=department_id).order_by('order')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.department:
            self.fields['role'].queryset = self.instance.department.role_set.all().order_by('order')
        else:
            self.fields['role'].queryset = Role.objects.none()


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


class InvestigationRequestForm(forms.ModelForm):
    class Meta:
        model = InvestigationRequest
        fields = [
            'first_name', 'last_name', 'address', 'passport_link',
            'phone_number', 'title', 'description', 'image'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'passport_link': forms.URLInput(attrs={'class': 'form-control', 'required': True}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'required': True, 'pattern': r'\d{3}-\d{3}(-\d{1,3})?'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'required': True}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
