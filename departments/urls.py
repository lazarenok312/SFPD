from django.urls import path
from . import views

app_name = 'departments'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('police_academy/', views.pa_view, name='pa_detail'),
    path('cpd/', views.cpd_view, name='cpd_detail'),
    path('swat/', views.swat_view, name='swat_detail'),
    path('seb/', views.seb_view, name='seb_detail'),
    path('db/', views.db_view, name='db_detail'),
    path('about/', views.about_view, name='about'),
    path('faq/', views.faq_view, name='faq'),
    path('faq/', views.faq_view, name='faq'),
    path('hall_of_fame/', views.hall_fame, name='hall_of_fame'),
    path('thank_board/', views.thank_board, name='thank_board'),
    path('police-academy/', views.police_academy_view, name='police_academy_view'),
    path('department-staff/', views.edit_department_staff, name='edit_department_staff'),
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('unsubscribe/<str:token>/', views.unsubscribe_view, name='unsubscribe'),
    path('change-history/', views.change_history_list, name='change_history_list'),
]
