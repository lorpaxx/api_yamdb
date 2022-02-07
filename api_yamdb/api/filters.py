from django_filters import FilterSet, rest_framework
from reviews.models import Title


class TitleFilter(FilterSet):

    category = rest_framework.CharFilter(
        field_name='category__slug',
    )
    genre = rest_framework.CharFilter(
        field_name='genre__slug'
    )
    name = rest_framework.CharFilter(
        field_name='name',
        lookup_expr='contains'
    )

    class Meta:
        model = Title
        fields = ('name', 'year')
