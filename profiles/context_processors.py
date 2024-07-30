from .forms import SupportForm
from .utils import get_unseen_counts

def add_support_form(request):
    return {'support_form': SupportForm()}


def notification_counts(request):
    return get_unseen_counts(request.user)
