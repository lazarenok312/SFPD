from django.urls import path
from profiles import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('check_username/', views.check_username, name='check_username'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

    path('profile/<slug:slug>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('support/', views.SupportView.as_view(), name='support'),
    path('profiles_list/', profile_list, name='profile_list'),
    path('profile/<slug:slug>/like/', views.like_profile, name='like_profile'),
    path('profile/<slug:slug>/dislike/', views.dislike_profile, name='dislike_profile'),
    path('ajax/load-roles/', views.load_roles, name='ajax_load_roles'),

    path('confirm/<str:token>/', views.confirm_profile, name='confirm_profile'),
    path('send-confirmation-email/', views.send_confirmation_email_view, name='send_confirmation_email'),
    path('request-role-confirmation/', request_role_confirmation, name='request_role_confirmation'),
    path('admin/confirm-roles/', views.confirm_roles, name='confirm_roles'),
    path('confirm_role/<int:profile_id>/', views.confirm_role, name='confirm_role'),

    path('investigations/', views.investigation_list, name='investigation_list'),
    path('investigation/new/', views.create_investigation_request, name='create_investigation_request'),
    path('investigation/<int:pk>/', views.investigation_detail, name='investigation_detail'),
    path('take-investigation/<int:pk>/', views.take_investigation, name='take_investigation'),
    path('release-investigation/<int:pk>/', views.release_investigation, name='release_investigation'),
    path('investigation/<int:pk>/response/', views.submit_response, name='submit_response'),
    path('close-investigation/<int:pk>/', close_investigation, name='close_investigation'),
]
