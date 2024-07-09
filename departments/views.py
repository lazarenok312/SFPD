from django.shortcuts import render
from profiles.models import EmployeeProfile


def home_view(request):
    departments = {
        'pa': {'name': 'Police Academy', 'role': 'Chief of PA', 'username': None},
        'cpd': {'name': 'Central Patrol Division', 'role': 'Chief of CPD', 'username': None},
        'swat': {'name': 'SWAT', 'role': 'Commander of SWAT', 'username': None},
        'db': {'name': 'Detective Bureau', 'role': 'Head of DB', 'username': None},
    }

    for key, department in departments.items():
        try:
            employee_profile = EmployeeProfile.objects.get(role__name=department['role'], department__name=department['name'])
            department['username'] = employee_profile.user.username
        except EmployeeProfile.DoesNotExist:
            department['username'] = None

    context = {f"{key}_username": department['username'] for key, department in departments.items()}
    return render(request, 'home/index.html', context)