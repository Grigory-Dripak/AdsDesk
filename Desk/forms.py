from django import forms
from tinymce.widgets import TinyMCE
from .models import Ads, Category

cats = Category.objects.all().values('pk', 'name')
catchoice = []

for i in cats:
    catchoice.append((i['pk'], i['name']))


class AdsForm(forms.ModelForm):
    category = forms.ChoiceField(label='Категория', choices=catchoice)
    title = forms.CharField(label='Заголовок')
    content = forms.CharField(label='Детальная информация', widget=TinyMCE())

    class Meta:
        model = Ads
        fields = ['category',
                  'title',
                  'content',
                  ]
