from django import forms
from .models import *
from django.forms import modelformset_factory


class PoliceAcademyPositionForm(forms.ModelForm):
    class Meta:
        model = PoliceAcademyPosition
        fields = ['position', 'nickname', 'description', 'photo']
        widgets = {
            'position': forms.Select(attrs={'class': 'form-input'}),
            'nickname': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input'}),
            'photo': forms.FileInput(attrs={'class': 'form-input photo-input'}),
        }
        labels = {
            'position': 'Должность',
            'nickname': 'Никнейм',
            'description': 'Описание',
            'photo': 'Фотография',
        }


PoliceAcademyPositionFormSet = forms.modelformset_factory(
    PoliceAcademyPosition,
    form=PoliceAcademyPositionForm,
    extra=0,
    can_delete=False
)


class DepartmentStaffForm(forms.ModelForm):
    class Meta:
        model = DepartmentStaff
        fields = ['title', 'name', 'job_title', 'discord_url', 'vk_url', 'photo']
        widgets = {
            'title': forms.Select(attrs={'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'job_title': forms.TextInput(attrs={'class': 'form-input'}),
            'discord_url': forms.TextInput(attrs={'class': 'form-input'}),
            'vk_url': forms.TextInput(attrs={'class': 'form-input'}),
            'photo': forms.FileInput(attrs={'class': 'form-input photo-input'}),
        }
        labels = {
            'title': 'Звание',
            'name': 'Никнейм',
            'job_title': 'Должность',
            'discord_url': 'Дискорд',
            'vk_url': 'ВК',
            'photo': 'Фотография',
        }


DepartmentStaffFormSet = modelformset_factory(
    DepartmentStaff,
    form=DepartmentStaffForm,
    extra=0,
    can_delete=False
)
