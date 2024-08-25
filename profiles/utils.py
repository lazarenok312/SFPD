from django.utils import timezone
from news.models import News
from departments.models import ChangeHistory


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
