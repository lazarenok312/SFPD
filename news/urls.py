from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('news/<int:pk>/add_comment/', views.add_comment, name='add_comment'),
    path('news/<int:pk>/like/', views.like_news, name='like_news'),
    path('news/<int:pk>/dislike/', views.dislike_news, name='dislike_news'),
    path('comment/<int:pk>/delete/', views.DeleteCommentView.as_view(), name='delete_comment'),
]
