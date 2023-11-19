from django.conf import settings
from django.db import models
from django.urls import reverse

from mailing.models import NULLABLE


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    content = models.TextField(verbose_name='Content')
    slug = models.CharField(max_length=200, verbose_name='Slug')
    image = models.ImageField(upload_to='blog/', **NULLABLE, verbose_name='Image',)
    is_published = models.BooleanField(default=False, verbose_name='Published')
    views_count = models.IntegerField(default=0, verbose_name='Views count')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Created date')
    modified_date = models.DateTimeField(auto_now=True, verbose_name='Modified date')
    # published_date = models.DateTimeField(**NULLABLE, verbose_name='Published date')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   **NULLABLE, verbose_name='Created by')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:articles', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'article'
        verbose_name_plural = 'articles'
        ordering = ('-created_date',)
        # permissions = [('set_published_status', 'Can publish article')].
