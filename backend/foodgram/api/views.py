import pandas as pd
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.views import UserViewSet

from .viewsets import RetrieveListViewset
from recipes.models import (Tag, Recipe, Ingredient, 
                            Favourite, ShoppingCart, RecipeIngredient,
                            Follow, User)

from .serializers import (TagSerializer, RecipeSerializer, IngredientSerializer,
                          RecipeShortSerializer, UserSerializer)


class TagViewSet(RetrieveListViewset):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options', 'trace']
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('tags', 'author', 'is_in_shopping_cart')

    def perform_create(self, serializer):
        current_user = self.request.user
        serializer.save(author=current_user)
    
    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk=None):
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
    
    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        user = request.user
        data = RecipeIngredient.objects.filter(
            recipe__shopping_cart__owner=user
            ).values('ingredient__name', 'ingredient__unit'
            ).annotate(amount=Sum('amount'))
        content = pd.DataFrame(data).to_string(header=None, index=None)

        return FileResponse(content, content_type='text/plain')

class IngredientViewSet(RetrieveListViewset):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class UserViewSet(UserViewSet):

    @action(methods=['post'], detail=True)
    def subscribe(self, request, **kwargs):
        user = request.user
        user_id = kwargs['id']
        following = get_object_or_404(User, pk=user_id)
        Follow.objects.get_or_create(user=user, author=following)
        serializer = UserSerializer(instance=following)
        return Response(serializer.data, status=status.HTTP_201_CREATED)