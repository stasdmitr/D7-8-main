from django.urls import path, include
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('news/', NewsList.as_view(), name='news'),
    path('articles/', ArticlesList.as_view(), name='articles'),
    path('news/<int:pk>', cache_page(60 * 10)(NewsDetail.as_view()), name='news_detail'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('news/search/', NewsSearch.as_view(), name='news_search'),
    path('articles/<int:pk>', cache_page(60 * 10)(ArticlesDetail.as_view()), name='articles_detail'),
    path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/update/', ArticlesUpdate.as_view(), name='articles_update'),
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
    path('make_appointment/', AppointmentView.as_view(), name='make_appointment'),
]
