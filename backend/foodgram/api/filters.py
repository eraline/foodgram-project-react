from django_filters import rest_framework as filters

from recipes.models import Recipe

class RecipeFilter(filters.FilterSet):
    is_in_shopping_cart = filters.BooleanFilter()
    is_favorite = filters.BooleanFilter()
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    class Meta:
        model = Recipe
        fields = ['user', 'is_in_shopping_cart', 'is_favorite', 'tags']