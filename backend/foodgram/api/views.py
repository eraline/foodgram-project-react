import pandas as pd
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Exists, OuterRef
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.views import UserViewSet

from .viewsets import RetrieveListViewset
from .filters import RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnly
from recipes.models import (Tag, Recipe, Ingredient, 
                            Favourite, ShoppingCart, RecipeIngredient,
                            Follow, User)

from .serializers import (TagSerializer, RecipeSerializer, IngredientSerializer,
                          RecipeShortSerializer, UserSerializer, SubscriptionSerializer)


class TagViewSet(RetrieveListViewset):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options', 'trace']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPagination
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            user_id = -1
        else:
            user_id = user.pk
        
        queryset = Recipe.objects.all().annotate(
            is_in_shopping_cart=Exists(
                ShoppingCart.objects.filter(user__pk=user_id, recipe=OuterRef('pk'))
                ),
            is_favorited=Exists(
                Favourite.objects.filter(user__pk=user_id, recipe=OuterRef('pk'))
                )
        ).order_by('-created_at', '-pk')
        return queryset

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
                recipe=recipe, user=request.user)
            serializer = RecipeShortSerializer(instance=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        obj = get_object_or_404(
            ShoppingCart,
            recipe=recipe,
            user=request.user)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(methods=['get'], detail=False)
    def download_shopping_cart(self, request):
        user = request.user
        data = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=user
            ).values('ingredient__name', 'ingredient__measurement_unit'
            ).annotate(amount=Sum('amount'))
        content = pd.DataFrame(data).to_string(header=None, index=None)

        return FileResponse(content, content_type='text/plain')

class IngredientViewSet(RetrieveListViewset):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class UserViewSet(UserViewSet):
    
    serializer_class = UserSerializer
#     pagination_class = CustomPagination

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, **kwargs):
        user = request.user
        following_id = kwargs['id']
        following = get_object_or_404(User, pk=following_id)
        if request.method == 'POST':
            Follow.objects.get_or_create(user=user, following=following)
            context = {'request': request}
            serializer = SubscriptionSerializer(instance=following, context=context)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        obj = get_object_or_404(Follow, user=user, following=following)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def subscriptions(self, request):
        pagination = CustomPagination()
        user = request.user
        queryset = User.objects.filter(following__user=user)
        qs = pagination.paginate_queryset(queryset, request)
        context = {'request': request}
        serializer = SubscriptionSerializer(qs, context=context, many=True)
        return pagination.get_paginated_response(serializer.data)