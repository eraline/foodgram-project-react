from django_filters import rest_framework as filters
from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    is_in_shopping_cart = filters.BooleanFilter()
    is_favorited = filters.BooleanFilter()
    tags = filters.ModelMultipleChoiceFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ['author', 'is_in_shopping_cart', 'is_favorited', 'tags']
