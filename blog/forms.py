from django import forms

from blog.models import Article
from users.forms import StyleFormMixin


class ArticleForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'content', 'image')
