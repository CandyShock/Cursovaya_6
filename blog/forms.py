from blog.models import Blog
from mailing.forms import StyleFormMixin
from django import forms


class PostForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        exclude = ('views',)
