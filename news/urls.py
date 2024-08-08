from django.urls import path
from . import views

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_list'),
    path('<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('<int:pk>/like/', views.like_news, name='like_news'),
    path('<int:pk>/dislike/', views.dislike_news, name='dislike_news'),
    path('comment/<int:pk>/delete/', views.DeleteCommentView.as_view(), name='delete_comment'),
]
