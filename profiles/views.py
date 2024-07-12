from profiles.forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DetailView
from .models import Profile
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm
from django.views.generic import View
from departments.models import Role
from django.http import JsonResponse


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, f"Аккаунт для пользователя {user.username} создан,<br>Добро пожаловать!")
            return redirect(reverse_lazy('departments:home'))
        else:
            for field in user_form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            for error in user_form.non_field_errors():
                messages.error(request, error)
    else:
        user_form = UserRegistrationForm()
    return render(request, 'profiles/register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.username}!")

            return redirect(reverse_lazy('departments:home'))

        else:
            messages.error(request, 'Неправильный логин или пароль')

    return render(request, 'profiles/login.html')


def user_logout(request):
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.success(request, f"До скорых встреч, {username}!")
    return redirect('departments:home')


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile/profile_detail.html'
    context_object_name = 'profile'
    slug_field = 'slug'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ProfileUpdateForm(request.POST, request.FILES, instance=self.object)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile_detail', slug=self.object.slug)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = ProfileUpdateForm(instance=self.object)
        return context


class LoadRolesView(View):
    def get(self, request):
        department_id = request.GET.get('department_id')
        roles = Role.objects.filter(department_id=department_id).values('id', 'name')
        return JsonResponse(list(roles), safe=False)
