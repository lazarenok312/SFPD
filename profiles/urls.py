from django.urls import path
from profiles import views
from .views import *

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/<slug:slug>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('load_roles/', LoadRolesView.as_view(), name='load_roles'),
]
