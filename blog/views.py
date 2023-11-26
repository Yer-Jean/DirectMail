from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.forms import ArticleForm
from blog.models import Article
from mailing.services import get_cache


class ArticleListView(ListView):
    model = Article

    def get_queryset(self):
        # Получаем данные из кэша, если они есть.
        # Если нет, то запрашиваем у БД используя фильтр, указанный в kwargs

        # Для группы Managers показываем все статьи блога, включая не опубликованные
        if self.request.user.role('managers'):
            kwargs = {}
        else:
            kwargs = {'is_published': True}

        queryset = get_cache(self.model, kwargs)
        return queryset


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm

    def get_success_url(self):
        return reverse('blog:article_view', args=[self.object.slug])

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.slug = slugify(self.object.title)
            self.object.created_by = self.request.user
            self.object.save()

        return super().form_valid(form)


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1  # Увеличиваем счетчик просмотров
        self.object.save()
        return self.object


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.created_by != self.request.user:
            raise Http404
        return self.object

    def get_success_url(self):
        return reverse('blog:article_view', args=[self.object.slug])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['blog'] = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        return context_data

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.slug = slugify(self.object.title)
            self.object.save()

        return super().form_valid(form)


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('blog:articles')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.created_by != self.request.user:
            raise Http404
        return self.object


@permission_required('blog.set_published_status')
def toggle_publish(request, pk):
    article = Article.objects.get(pk=pk)
    # Переключаем статус is_published
    article.is_published = {article.is_published: False,
                            not article.is_published: True}[True]
    article.save()
    return redirect(reverse('blog:articles'))
