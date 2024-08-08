from django.views.generic import ListView, DetailView
from .models import News, Comment, LikeDislike
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from profiles.models import Profile


class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        return News.objects.order_by('-created_at')

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            profile.last_viewed_news = timezone.now()
            profile.save()
        return response


class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.order_by('-created_at')
        return context


def add_comment(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comment.objects.create(user=request.user, news=news, content=content)
            data = {
                'success': True,
                'comment': {
                    'id': comment.pk,
                    'user': {
                        'username': comment.user.username,
                    },
                    'content': comment.content,
                    'created_at': comment.created_at.strftime("%d %b %Y %H:%M"),
                }
            }
            return JsonResponse(data)
    return JsonResponse({'success': False})


@method_decorator(login_required, name='dispatch')
class DeleteCommentView(View):
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.user == request.user:
            comment.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'У вас нет прав на удаление этого комментария.'})


def like_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    user = request.user
    liked = LikeDislike.objects.filter(news=news, user=user, vote=LikeDislike.LIKE).exists()
    disliked = LikeDislike.objects.filter(news=news, user=user, vote=LikeDislike.DISLIKE).exists()

    if not liked:
        LikeDislike.objects.update_or_create(news=news, user=user, defaults={'vote': LikeDislike.LIKE})
        if disliked:
            LikeDislike.objects.filter(news=news, user=user, vote=LikeDislike.DISLIKE).delete()

    return JsonResponse({
        'total_likes': news.total_likes(),
        'total_dislikes': news.total_dislikes(),
    })


def dislike_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    user = request.user
    liked = LikeDislike.objects.filter(news=news, user=user, vote=LikeDislike.LIKE).exists()
    disliked = LikeDislike.objects.filter(news=news, user=user, vote=LikeDislike.DISLIKE).exists()

    if not disliked:
        LikeDislike.objects.update_or_create(news=news, user=user, defaults={'vote': LikeDislike.DISLIKE})
        if liked:
            LikeDislike.objects.filter(news=news, user=user, vote=LikeDislike.LIKE).delete()

    return JsonResponse({
        'total_likes': news.total_likes(),
        'total_dislikes': news.total_dislikes(),
    })
