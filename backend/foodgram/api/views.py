from email.errors import InvalidMultipartContentTransferEncodingDefect
from rest_framework import viewsets
from .viewsets import RetrieveListViewset, CreateDeleteViewSet
from recipes.models import Tag, Recipe, Ingredient, Favourite
from .serializers import TagSerializer, RecipeSerializer, IngredientSerializer, FavouriteSerializer


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
    

class IngredientViewSet(RetrieveListViewset):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class FavouritesViewSet(CreateDeleteViewSet):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = Recipe.objects.get(pk=recipe_id)
        serializer.save(user=self.request.user, recipe=recipe)

    def destroy(self, request):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = Recipe.objects.get(pk=recipe_id)
        Favourite.objects.filter(recipe=recipe, user=self.request.user).delete()
