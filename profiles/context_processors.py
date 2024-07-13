from .forms import SupportForm


def add_support_form(request):
    return {'support_form': SupportForm()}
