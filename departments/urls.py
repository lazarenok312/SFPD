from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('police_academy/', views.pa_view, name='pa_detail'),
    path('cpd/', views.cpd_view, name='cpd_detail'),
    path('swat/', views.swat_view, name='swat_detail'),
    path('db/', views.db_view, name='db_detail'),
    path('about/', views.about_view, name='about'),
    path('faq/', views.faq_view, name='faq'),
]