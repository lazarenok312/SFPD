from profiles.forms import UserRegistrationForm, ProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, f"Аккаунт создан для пользователя {user.username}!")
            return redirect(reverse_lazy('user_login'))
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
        messages.success(request, f"До свидания, {username}!")
    return redirect('departments:home')
