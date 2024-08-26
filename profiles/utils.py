from django.utils import timezone
from news.models import News
from departments.models import ChangeHistory
from profiles.models import Profile, InvestigationRequest

def get_unseen_counts(user):
    if not user.is_authenticated:
        return {'new_news_count': 0, 'new_changes_count': 0, 'role_confirmation_count': 0, 'total_unseen': 0, 'available_requests_count': 0}

    profile = user.profile
    now = timezone.now()

    new_news_count = News.objects.filter(
        created_at__gt=profile.last_viewed_news).count() if profile.last_viewed_news else News.objects.count()

    new_changes_count = ChangeHistory.objects.filter(
        created_at__gt=profile.last_viewed_changes).count() if profile.last_viewed_changes else ChangeHistory.objects.count()

    role_confirmation_count = Profile.objects.filter(
        role_confirmation_requested=True, role_confirmed=False).count()

    available_requests_count = InvestigationRequest.objects.filter(
        is_closed=False, assigned_to__isnull=True).count()

    total_unseen = new_changes_count + role_confirmation_count

    return {
        'new_news_count': new_news_count,
        'new_changes_count': new_changes_count,
        'role_confirmation_count': role_confirmation_count,
        'total_unseen': total_unseen,
        'available_requests_count': available_requests_count,
    }
