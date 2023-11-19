from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Article


class ArticleListView(ListView):
    model = Article

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        # queryset = queryset.order_by('-created_at')
        return queryset


class ArticleCreateView(CreateView):
    model = Article
    fields = ('title', 'content', 'image',)

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


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ['title', 'content', 'image', 'is_published']

    def get_success_url(self):
        return reverse('blog:article', args=[self.kwargs.get('pk')])

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


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('blog:articles')
