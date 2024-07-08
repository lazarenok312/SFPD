from django.urls import path
from profiles import views

urlpatterns = [
    path('register/', views.register, name='register'),
]