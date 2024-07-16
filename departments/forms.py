from django import forms
from .models import PoliceAcademyPosition
from django.forms import modelformset_factory


class PoliceAcademyPositionForm(forms.ModelForm):
    class Meta:
        model = PoliceAcademyPosition
        fields = ['position', 'nickname', 'description', 'photo']
        widgets = {
            'position': forms.Select(attrs={'class': 'form-input'}),
            'nickname': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input'}),
            'photo': forms.FileInput(attrs={'class': 'form-input'}),
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