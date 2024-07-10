from django.urls import path
from .views import home_view
from . import views

urlpatterns = [
    path('', home_view, name='home'),
    path('department/police_academy', views.pa_view, name='pa_detail'),
    path('department/cpd', views.cpd_view, name='cpd_detail'),
    path('department/swat', views.swat_view, name='swat_detail'),
    path('department/db', views.db_view, name='db_detail'),
    path('department/about', views.about_view, name='about'),
    path('faq', views.faq_view, name='faq'),
]
