from django.urls import path
from django.views.decorators.cache import cache_page

from .apps import BlogConfig
from .views import ArticleListView, ArticleCreateView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView, \
    toggle_publish

app_name = BlogConfig.name

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('article/create/', ArticleCreateView.as_view(), name='article_create'),
    path('article/view/<str:slug>/', cache_page(300)(ArticleDetailView.as_view()), name='article_view'),
    path('article/update/<int:pk>/', ArticleUpdateView.as_view(), name='article_update'),
    path('article/delete/<int:pk>', ArticleDeleteView.as_view(), name='article_delete'),
    path('article/toggle_publish/<int:pk>', toggle_publish, name='toggle_publish'),
]
