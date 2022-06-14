from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .viewsets import RetrieveListViewset
from recipes.models import Tag, Recipe, Ingredient, Favourite, ShoppingCart
from .serializers import (TagSerializer, RecipeSerializer, IngredientSerializer,
                          RecipeShortSerializer)


class TagViewSet(RetrieveListViewset):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options', 'trace']

    def perform_create(self, serializer):
        current_user = self.request.user
        serializer.save(author=current_user)
    
    @action(methods=['post', 'delete'], detail=True)
    def favourite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            Favourite.objects.get_or_create(
                recipe=recipe, user=request.user)
            serializer = RecipeShortSerializer(instance=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        favourite = get_object_or_404(
            Favourite,
            recipe=recipe,
            user=request.user)
        favourite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            ShoppingCart.objects.get_or_create(
                recipe=recipe, owner=request.user)
            serializer = RecipeShortSerializer(instance=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        obj = get_object_or_404(
            ShoppingCart,
            recipe=recipe,
            owner=request.user)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class IngredientViewSet(RetrieveListViewset):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

# class FavouritesViewSet(CreateDeleteViewSet):
#     queryset = Favourite.objects.all()
#     serializer_class = FavouriteSerializer
# 
#     def perform_create(self, serializer):
#         recipe_id = self.kwargs.get('recipe_id')
#         recipe = Recipe.objects.get(pk=recipe_id)
#         serializer.save(user=self.request.user, recipe=recipe)
# 
#     def destroy(self, request):
#         recipe_id = self.kwargs.get('recipe_id')
#         recipe = Recipe.objects.get(pk=recipe_id)
#         Favourite.objects.filter(recipe=recipe, user=self.request.user).delete()
# 