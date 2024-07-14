from django import forms
from .models import PoliceAcademyPosition
from django.forms import modelformset_factory


class PoliceAcademyPositionForm(forms.ModelForm):
    class Meta:
        model = PoliceAcademyPosition
        fields = ['position', 'nickname', 'description', 'photo']


PoliceAcademyPositionFormSet = modelformset_factory(
    PoliceAcademyPosition,
    fields=('position', 'nickname', 'description', 'photo'),
    extra=0,
    can_delete=False
)
