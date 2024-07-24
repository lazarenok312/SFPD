from django.shortcuts import render, redirect, get_object_or_404
from .models import PoliceAcademyPosition
from .forms import *
from django.views.generic.edit import UpdateView, View
from django.http import HttpResponse
from django.contrib import messages


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
    sheriff = DepartmentStaff.objects.filter(title='sheriff').first()
    colonel1 = DepartmentStaff.objects.filter(title='colonel1').first()
    colonel2 = DepartmentStaff.objects.filter(title='colonel2').first()
    colonel3 = DepartmentStaff.objects.filter(title='colonel3').first()
    lcolonel1 = DepartmentStaff.objects.filter(title='lcolonel1').first()
    lcolonel2 = DepartmentStaff.objects.filter(title='lcolonel2').first()
    lcolonel3 = DepartmentStaff.objects.filter(title='lcolonel3').first()
    major1 = DepartmentStaff.objects.filter(title='major1').first()
    major2 = DepartmentStaff.objects.filter(title='major2').first()
    major3 = DepartmentStaff.objects.filter(title='major3').first()
    major4 = DepartmentStaff.objects.filter(title='major4').first()
    contract_service_status = ContractServiceStatus.objects.first()

    context = {
        'sheriff': sheriff,
        'colonel1': colonel1,
        'colonel2': colonel2,
        'colonel3': colonel3,
        'lcolonel1': lcolonel1,
        'lcolonel2': lcolonel2,
        'lcolonel3': lcolonel3,
        'major1': major1,
        'major2': major2,
        'major3': major3,
        'major4': major4,
        'contract_service_status': contract_service_status,
    }
    return render(request, 'departments/about_detail.html', context)


def hall_fame(request):
    return render(request, 'miscellaneous/hall_fame.html')


def thank_board(request):
    return render(request, 'miscellaneous/thank_board.html')


def change_history_list(request):
    changes = ChangeHistory.objects.all()
    return render(request, 'include/change_history_list.html', {'changes': changes})


def police_academy_view(request):
    positions = ['chief', 'dep_chief1', 'dep_chief2']

    for position in positions:
        PoliceAcademyPosition.objects.get_or_create(position=position)

    positions_qs = PoliceAcademyPosition.objects.filter(position__in=positions)

    if request.method == 'POST':
        formset = PoliceAcademyPositionFormSet(request.POST, request.FILES, queryset=positions_qs)
        if formset.is_valid():
            formset.save()
            return redirect('departments:pa_detail')
        else:
            print("Formset errors:", formset.errors)
            for form in formset:
                print(form.errors)
    else:
        formset = PoliceAcademyPositionFormSet(queryset=positions_qs)

    return render(request, 'forms/police_academy_form.html', {'formset': formset})


def edit_department_staff(request):
    if request.method == 'POST':
        formset = DepartmentStaffFormSet(request.POST, request.FILES, queryset=DepartmentStaff.objects.all())
        if formset.is_valid():
            formset.save()
            return redirect('departments:about')
        else:
            print("Formset errors:", formset.errors)
            for form in formset:
                print(form.errors)
    else:
        queryset = DepartmentStaff.objects.all()
        formset = DepartmentStaffFormSet(queryset=queryset)

    return render(request, 'forms/department_staff_form.html', {'formset': formset})


class ContractServiceStatusForm(forms.ModelForm):
    class Meta:
        model = ContractServiceStatus
        fields = ['is_active']


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']


class SubscribeView(View):
    def post(self, request):
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно подписались на уведомления!")
        else:
            messages.error(request, "Произошла ошибка при подписке. Пожалуйста, попробуйте еще раз.")
        return redirect('departments:about')


def unsubscribe_view(request, token):
    try:
        unsubscribe_token = UnsubscribeToken.objects.get(token=token)
        if unsubscribe_token.is_valid():
            Subscriber.objects.filter(email=unsubscribe_token.email).delete()
            unsubscribe_token.delete()
            return HttpResponse("Вы успешно отписались от рассылки.")
        else:
            return HttpResponse("Этот токен для отписки недействителен или истек.")
    except UnsubscribeToken.DoesNotExist:
        return HttpResponse("Токен не найден.")
