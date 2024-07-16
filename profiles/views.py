from profiles.forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DetailView
from .models import Profile
from django.shortcuts import render, redirect
from .forms import ProfileUpdateForm, SupportForm
from django.views.generic import View
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import ProfileChangeLog
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


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


@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile/profile_detail.html'
    context_object_name = 'profile'
    slug_field = 'slug'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.method == "POST" and self.object.user != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            raise PermissionDenied
        form = ProfileUpdateForm(request.POST, request.FILES, instance=self.object)
        # if form.is_valid():
        #     form.save()
        #     messages.success(request, 'Профиль успешно обновлен!')
        #     return redirect('profile_detail', slug=self.object.slug)
        # return self.render_to_response(self.get_context_data(form=form))

        if form.is_valid():
            old_profile_data = Profile.objects.get(pk=self.object.pk)

            new_profile_data = form.save()

            changes_logged = False
            for field_name, new_value in form.cleaned_data.items():
                old_value = getattr(old_profile_data, field_name)
                if old_value != new_value:
                    change_type = f"Changed {field_name}"
                    ProfileChangeLog.objects.create(user=request.user, change_type=change_type,
                                                    old_value=old_value, new_value=new_value)
                    changes_logged = True

            if changes_logged:
                messages.success(request, 'Профиль успешно обновлен!')
            else:
                messages.info(request, 'Нет изменений в профиле для логирования.')

            return redirect('profile_detail', slug=self.object.slug)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = ProfileUpdateForm(instance=self.object)
        context['can_edit'] = self.object.user == self.request.user
        return context


class SupportView(View):
    def get(self, request):
        form = SupportForm()
        return render(request, 'include/footer.html', {'form': form})

    def post(self, request):
        form = SupportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваше обращение успешно доставлено!')
            return redirect(request.META.get('HTTP_REFERER', 'departments:home'))
        return render(request, 'include/footer.html', {'form': form})


# class SupportView(View):
#     def get(self, request):
#         form = SupportForm()
#         return render(request, 'include/footer.html', {'form': form})
#
#     def post(self, request):
#         form = SupportForm(request.POST)
#         if form.is_valid():
#             support_request = form.save()
#
#             # Отправляем ответное сообщение на указанный email
#             subject = 'Ваше обращение принято'
#             message = 'Благодарим вас за обращение. Мы обработаем его в ближайшее время.'
#             from_email = settings.EMAIL_HOST_USER
#             to_email = form.cleaned_data['email']
#             send_mail(subject, message, from_email, [to_email])
#
#             messages.success(request, 'Ваше обращение успешно доставлено!')
#             return redirect(request.META.get('HTTP_REFERER', 'departments:home'))
#         return render(request, 'include/footer.html', {'form': form})

def profile_list(request):
    profiles = Profile.objects.order_by('id').all()  # Ensure ordering
    query = request.GET.get('q')
    if query:
        profiles = profiles.filter(
            Q(name__icontains=query) | Q(nick_name__icontains=query)
        )

    paginator = Paginator(profiles, 10)
    page = request.GET.get('page')
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        profiles = paginator.page(1)
    except EmptyPage:
        profiles = paginator.page(paginator.num_pages)

    return render(request, 'profiles/profile_list.html', {'profiles': profiles})
