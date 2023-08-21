from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter
from .models import Category, Reply, Ads, STATUS


class ReplyFilter(FilterSet):

    category = ModelChoiceFilter(
        field_name="reply_to__category",
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='all',
    )

    class Meta:
        model = Reply
        fields = {
            'reply': ['icontains'],
        }

