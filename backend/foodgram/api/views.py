from rest_framework import viewsets
from rest_framework import permissions
from .viewsets import RetrieveListViewset
from recipes.models import Tag, Recipe, Ingredient
from .serializers import TagSerializer, RecipeSerializer, IngredientSerializer


class TagViewSet(RetrieveListViewset):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        current_user = self.request.user
        serializer.save(author=current_user)

class IngredientViewSet(RetrieveListViewset):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer