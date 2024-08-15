from SFPD.settings import SITE_DOMAIN, DEFAULT_FROM_EMAIL
from profiles.forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import DetailView, View
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ProfileUpdateForm, SupportForm
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings
from django.template.loader import render_to_string
from departments.models import ChangeHistory
from news.models import News
from datetime import timedelta


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            if not Profile.objects.filter(user=user).exists():
                reg_role = user_form.cleaned_data.get('reg_role')
                Profile.objects.create(user=user, reg_role=reg_role)

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

    context = {
        'user_form': user_form,
    }

    return render(request, 'profiles/register.html', context)


def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username=username).exists()
    }
    return JsonResponse(data)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем не найден.')
            return render(request, 'profiles/login.html')

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

        if form.is_valid():
            old_profile_data = Profile.objects.get(pk=self.object.pk)
            new_profile_data = form.save(commit=False)

            for field in form.cleaned_data:
                if field == 'photo' or form.cleaned_data[field]:
                    setattr(new_profile_data, field, form.cleaned_data[field])

            new_profile_data.save()

            changes_logged = False
            for field_name, new_value in form.cleaned_data.items():
                old_value = getattr(old_profile_data, field_name)

                if new_value is None:
                    new_value = ''
                if old_value is None:
                    old_value = ''

                if old_value != new_value:
                    change_type = f"Changed {field_name}"
                    ProfileChangeLog.objects.create(
                        user=request.user,
                        change_type=change_type,
                        old_value=str(old_value),
                        new_value=str(new_value)
                    )
                    changes_logged = True

            if changes_logged:
                messages.success(request, 'Профиль успешно обновлен!')
            else:
                messages.info(request, 'Нет изменений для логирования.')

            return redirect('profile_detail', slug=self.object.slug)

        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'form' not in context:
            context['form'] = ProfileUpdateForm(instance=self.object)

        context['can_edit'] = self.object.user == self.request.user
        context['departments'] = Department.objects.all()
        context['is_editor'] = self.object.is_editor()

        if self.object and self.object.department:
            context['roles'] = self.object.department.role_set.all().order_by('order')
        else:
            context['roles'] = Role.objects.none()

        user_groups = self.object.user.groups.all()
        context['user_groups'] = user_groups
        context['is_moderator'] = self.object.user.groups.filter(
            name__in=["Модератор", "Редактор", "Руководитель"]).exists()

        next_level_threshold = self.object.get_next_level_threshold()

        if next_level_threshold > 0:
            context['rating_percentage'] = int(min((self.object.rating / next_level_threshold) * 100, 100))
        else:
            context['rating_percentage'] = 0

        if context['rating_percentage'] < 33:
            context['progress_color'] = '#ff4c4c'
        elif context['rating_percentage'] < 66:
            context['progress_color'] = '#ffc107'
        else:
            context['progress_color'] = '#28a745'

        return context


def award_points_for_action(user, action_type):
    profile = user.profile
    if action_type == 'like':
        points = 8
    elif action_type == 'comment':
        points = 12
    elif action_type == 'visit':
        points = 1
    else:
        points = 0

    recent_activity = ActivityLog.objects.filter(
        profile=profile,
        activity_type=action_type,
        timestamp__gte=timezone.now() - timedelta(minutes=2)
    ).exists()

    if not recent_activity:
        ActivityLog.objects.create(profile=profile, activity_type=action_type, points=points)

        profile.update_rating(points)



def load_roles(request):
    department_id = request.GET.get('department')
    roles = Role.objects.filter(department_id=department_id).order_by('order').values('id', 'name')
    return JsonResponse(list(roles), safe=False)


class SupportView(View):
    def get(self, request):
        form = SupportForm()
        return render(request, 'include/footer.html', {'form': form})

    def post(self, request):
        form = SupportForm(request.POST)
        if form.is_valid():
            support_request = form.save()

            subject = 'Ваше обращение принято'
            message = 'Благодарим вас за обращение. Мы обработаем его в ближайшее время.'
            from_email = settings.EMAIL_HOST_USER
            to_email = form.cleaned_data['email']

            try:
                send_mail(subject, message, from_email, [to_email])
                messages.success(request, 'Ваше обращение успешно доставлено!')
            except Exception as e:
                messages.error(request, f'Ошибка при отправке письма: {e}')

            return redirect(request.META.get('HTTP_REFERER', 'departments:home'))
        return render(request, 'include/footer.html', {'form': form})


def profile_list(request):
    query = request.GET.get('q', '')
    profiles = Profile.objects.all()

    if query:
        profiles = profiles.filter(
            Q(name__icontains=query) | Q(surnames__icontains=query) | Q(nick_name__icontains=query)
        )

    profiles = profiles.order_by('-level')

    paginator = Paginator(profiles, 25)
    page = request.GET.get('page', 1)
    try:
        profiles_page = paginator.page(page)
    except PageNotAnInteger:
        profiles_page = paginator.page(1)
    except EmptyPage:
        profiles_page = paginator.page(paginator.num_pages)

    def get_level_class(level):
        if level < 5:
            return 'bg-gradient-blue'
        elif level < 10:
            return 'bg-gradient-green'
        elif level < 20:
            return 'bg-gradient-yellow'
        else:
            return 'bg-gradient-danger'

    for profile in profiles_page:
        profile.level_class = get_level_class(profile.level)

    total_profiles = profiles.count()
    start_record = (profiles_page.number - 1) * paginator.per_page + 1
    end_record = start_record + profiles_page.paginator.per_page - 1
    if end_record > total_profiles:
        end_record = total_profiles

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('profiles/profile_table_body.html', {
            'profiles': profiles_page,
            'total_profiles': total_profiles,
            'start_record': start_record,
            'end_record': end_record,
        }, request=request)
        return JsonResponse({'html': html})

    departments = Department.objects.all()
    roles = Role.objects.all()

    return render(request, 'profiles/profile_list.html', {
        'profiles': profiles_page,
        'departments': departments,
        'roles': roles,
        'total_profiles': total_profiles,
        'start_record': start_record,
        'end_record': end_record,
    })


@login_required
def like_profile(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    like_dislike, created = LikeDislike.objects.get_or_create(user=request.user, profile=profile)

    if not created and like_dislike.is_like:
        like_dislike.delete()
        profile.likes -= 1
    elif not created and not like_dislike.is_like:
        like_dislike.is_like = True
        like_dislike.save()
        profile.likes += 1
        profile.dislikes -= 1
    else:
        like_dislike.is_like = True
        like_dislike.save()
        profile.likes += 1
        award_points_for_action(request.user, 'like')

    profile.save()
    return JsonResponse({'likes': profile.likes, 'dislikes': profile.dislikes})


@login_required
def dislike_profile(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    like_dislike, created = LikeDislike.objects.get_or_create(user=request.user, profile=profile)

    if not created and not like_dislike.is_like:
        like_dislike.delete()
        profile.dislikes -= 1
    elif not created and like_dislike.is_like:
        like_dislike.is_like = False
        like_dislike.save()
        profile.dislikes += 1
        profile.likes -= 1
    else:
        like_dislike.is_like = False
        like_dislike.save()
        profile.dislikes += 1
        award_points_for_action(request.user, 'like')

    profile.save()
    return JsonResponse({'likes': profile.likes, 'dislikes': profile.dislikes})


@login_required
def send_confirmation_email_view(request):
    user = request.user
    profile = user.profile

    token, created = ProfileConfirmationToken.objects.get_or_create(user=user)
    if not created:
        token.generate_token()

    if not token.token:
        token.generate_token()

    send_confirmation_email(user.email, token.token, user)
    messages.success(request, 'Письмо с подтверждением отправлено на вашу почту.')
    return redirect('profile_detail', slug=profile.slug)


def send_confirmation_email(email, token, user):
    if not token:
        raise ValueError("Токен не может быть пустым.")

    confirmation_link = reverse('confirm_profile', kwargs={'token': token})
    full_link = f'{SITE_DOMAIN}{confirmation_link}'
    subject = 'Подтверждение профиля'
    message = f'Для подтверждения профиля перейдите по ссылке: {full_link}'
    send_mail(subject, message, DEFAULT_FROM_EMAIL, [email])

    EmailLog.objects.create(
        recipient=user.email,
        subject=subject,
        body=message,
        user=user
    )


def confirm_profile(request, token):
    confirmation_token = get_object_or_404(ProfileConfirmationToken, token=token)
    if confirmation_token.is_expired():
        messages.error(request, 'Срок действия токена истек.')
        return redirect('home')

    profile = confirmation_token.user.profile
    profile.profile_confirmed = True
    profile.save()
    messages.success(request, 'Профиль успешно подтвержден.')
    return redirect('profile_detail', slug=profile.slug)


def get_unseen_counts(user):
    if not user.is_authenticated:
        return {'new_news_count': 0, 'new_changes_count': 0}

    profile = user.profile
    now = timezone.now()
    new_news_count = News.objects.filter(
        created_at__gt=profile.last_viewed_news).count() if profile.last_viewed_news else News.objects.count()
    new_changes_count = ChangeHistory.objects.filter(
        created_at__gt=profile.last_viewed_changes).count() if profile.last_viewed_changes else ChangeHistory.objects.count()

    return {'new_news_count': new_news_count, 'new_changes_count': new_changes_count}
