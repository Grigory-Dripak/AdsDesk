from django_filters import FilterSet, ModelChoiceFilter, CharFilter
from .models import Category


class ReplyFilter(FilterSet):

    reply_to__category = ModelChoiceFilter(
        field_name="reply_to__category",
        queryset=Category.objects.all(),
        label='Категория публикации',
        empty_label='all',
    )

    reply_to__title = CharFilter(
        label='Заголовок публикации содержит',
        lookup_expr='icontains'
    )

    reply = CharFilter(
        label='Отклик содержит',
        lookup_expr='icontains'
    )
