from django.shortcuts import render, redirect
from .models import PoliceAcademyPosition
from .forms import *


def home_view(request):
    chief_of_pa = PoliceAcademyPosition.objects.filter(position='chief').first()

    return render(request, 'home/index.html', {'chief_of_pa': chief_of_pa})


def pa_view(request):
    chief_of_pa = PoliceAcademyPosition.objects.filter(position='chief').first()
    dep_chief1_of_pa = PoliceAcademyPosition.objects.filter(position='dep_chief1').first()
    dep_chief2_of_pa = PoliceAcademyPosition.objects.filter(position='dep_chief2').first()

    context = {
        'chief_of_pa': chief_of_pa,
        'dep_chief1_of_pa': dep_chief1_of_pa,
        'dep_chief2_of_pa': dep_chief2_of_pa,
    }
    return render(request, 'departments/pa_detail.html', context)


def cpd_view(request):
    return render(request, 'departments/cpd_detail.html')


def swat_view(request):
    return render(request, 'departments/swat_detail.html')


def db_view(request):
    return render(request, 'departments/db_detail.html')


def faq_view(request):
    return render(request, 'departments/faq.html')


def about_view(request):
    return render(request, 'departments/about_detail.html')


def hall_fame(request):
    return render(request, 'miscellaneous/hall_fame.html')


def thank_board(request):
    return render(request, 'miscellaneous/thank_board.html')


def police_academy_view(request):
    positions = ['chief', 'dep_chief1', 'dep_chief2']

    # Убедиться, что в базе данных есть только одна запись для каждой позиции
    for position in positions:
        PoliceAcademyPosition.objects.get_or_create(position=position)

    positions_qs = PoliceAcademyPosition.objects.filter(position__in=positions)

    if request.method == 'POST':
        formset = PoliceAcademyPositionFormSet(request.POST, request.FILES, queryset=positions_qs)
        if formset.is_valid():
            formset.save()
            return redirect('departments:home')
    else:
        formset = PoliceAcademyPositionFormSet(queryset=positions_qs)

    return render(request, 'forms/police_academy_form.html', {'formset': formset})
