from .models import ImportantNotification

def important_notification(request):
    notification = ImportantNotification.objects.filter(is_active=True).order_by('-created_at').first()
    return {'important_notification': notification}