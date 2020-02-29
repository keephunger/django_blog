from django import forms

from blog.models import Article


class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = Article

        fields = ['title', 'content']
