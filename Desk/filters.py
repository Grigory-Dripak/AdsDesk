import django.forms
from django.forms import DateTimeInput
from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter
from .models import Category, Reply, Ads, STATUS


class ReplyFilter(FilterSet):

    category = ModelChoiceFilter(
        field_name="reply_to__category",
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='all',
    )

    title = ModelChoiceFilter(
        field_name="reply_to__title",
        queryset=Ads.objects.all().values('title'),
        label='Заголовок публикации',
        empty_label='all',
        # widget=django.forms.ChoiceField
    )

    # title = ModelChoiceFilter(
    #     field_name="reply_to",
    #     queryset=Reply.objects.all().values('reply_to__title'),
    #     label='Заголовок публикации',
    #     empty_label='all',
    # )

    # status = ModelChoiceFilter(
    #     field_name="status",
    #     queryset=Reply.,
    #     label='Статус отклика',
    #     empty_label='all',
    # )

    time_creation = DateTimeFilter(
        field_name='time_creation',
        label='Дата и время создания',
        lookup_expr='gt',
        widget=DateTimeInput(
        # widget=DateInput(
            format='%Y-%m-%dT%H:%M',
            # format='%Y-%m-%d',
            attrs={'type': 'datetime-local'},
        ),
    )

    class Meta:
        model = Reply
        fields = {
            'reply': ['icontains'],
        }


class AdsFilter(FilterSet):

    category = ModelChoiceFilter(
        field_name="category",
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='all',
    )

    title = ModelChoiceFilter(
        field_name="title",
        queryset=Ads.objects.all(),
        label='Заголовок публикации',
        empty_label='all',
    )

    class Meta:
        model = Ads
        fields = {
            'title': ['icontains'],
        }