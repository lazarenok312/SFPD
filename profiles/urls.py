from django.urls import path
from profiles import views
from .views import *

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/<slug:slug>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('support/', views.SupportView.as_view(), name='support'),
    path('profiles_list/', profile_list, name='profile_list'),
    path('profile/<slug:slug>/like/', views.like_profile, name='like_profile'),
    path('profile/<slug:slug>/dislike/', views.dislike_profile, name='dislike_profile'),
    path('load-roles/', views.LoadRolesView.as_view(), name='load_roles'),
]
