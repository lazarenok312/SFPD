from django.urls import path
from .views import home_view
from . import views

urlpatterns = [
    path('', home_view, name='home'),
    path('department/police_academy', views.pa_view, name='pa_detail'),
    path('department/about', views.about_view, name='about'),
]
