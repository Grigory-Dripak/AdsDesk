from django import forms
from tinymce.widgets import TinyMCE
from .models import Ads, Category, Reply


def catchoice():
    cats = Category.objects.all().values('pk', 'name')
    choices = []
    for i in cats:
        choices.append((i['pk'], i['name']))
    return choices


class AdsForm(forms.ModelForm):
    category = forms.ChoiceField(label='Категория', choices=catchoice())
    title = forms.CharField(label='Заголовок')
    content = forms.CharField(label='Детальная информация', widget=TinyMCE())

    class Meta:
        model = Ads
        fields = ['category',
                  'title',
                  'content',
                  ]


class CodeForm(forms.Form):
    activate_code = forms.IntegerField(label='Проверочный код',
                                       widget=forms.TextInput(
                                           attrs={'class': 'form-control verify-code', 'type': 'text'}),
                                       required=True)


class ReplyForm(forms.ModelForm):
    reply = forms.CharField(label='Текст отклика', widget=forms.Textarea(attrs={'rows': 5, 'cols': 60}))

    class Meta:
        model = Reply
        fields = ['reply']
