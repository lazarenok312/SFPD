from django.shortcuts import render
from profiles.models import EmployeeProfile
from django.shortcuts import render, get_object_or_404
from .models import Department


def home_view(request):
    departments = {
        'pa': {'name': 'Police Academy', 'role': 'Chief of PA', 'username': None},
        'cpd': {'name': 'Central Patrol Division', 'role': 'Chief of CPD', 'username': None},
        'swat': {'name': 'SWAT', 'role': 'Commander of SWAT', 'username': None},
        'db': {'name': 'Detective Bureau', 'role': 'Head of DB', 'username': None},
    }

    for key, department in departments.items():
        try:
            employee_profile = EmployeeProfile.objects.get(role__name=department['role'],
                                                           department__name=department['name'])
            department['username'] = employee_profile.user.username
        except EmployeeProfile.DoesNotExist:
            department['username'] = None

    context = {f"{key}_username": department['username'] for key, department in departments.items()}
    return render(request, 'home/index.html', context)


def pa_view(request):
    return render(request, 'departments/pa_detail.html')


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
