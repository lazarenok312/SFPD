from django.shortcuts import render
from profiles.models import EmployeeProfile


def home_view(request):
    departments = [
        {'slug': 'pa', 'name': 'Police Academy', 'role': 'Chief of PA'},
        {'slug': 'cpd', 'name': 'Central Patrol Division', 'role': 'Chief of CPD'},
        {'slug': 'swat', 'name': 'SWAT', 'role': 'Commander of SWAT'},
        {'slug': 'db', 'name': 'Detective Bureau', 'role': 'Head of DB'},
        # Добавьте другие отделы по мере необходимости
    ]

    for department in departments:
        try:
            employee_profile = EmployeeProfile.objects.get(role__name=department['role'], department__name=department['name'])
            department['username'] = employee_profile.user.username
        except EmployeeProfile.DoesNotExist:
            department['username'] = None

    context = {'departments': departments}
    return render(request, 'home/index.html', context)