import django_filters
from foods.models import Recipe
from users.models import User


class RecipeFilter(django_filters.FilterSet):
    """Фильтерсет для вьюсета RecipesViewSet."""

    author = django_filters.CharFilter(
        field_name='author__id', lookup_expr='icontains')
    tags = django_filters.CharFilter(
        field_name='tags__slug', lookup_expr='icontains')
    is_favorited = django_filters.BooleanFilter(field_name='is_favorited')
    is_in_shopping_cart = django_filters.BooleanFilter(
        field_name='is_in_shopping_cart')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')
