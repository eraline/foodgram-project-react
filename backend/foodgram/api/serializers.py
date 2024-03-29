import base64
import datetime as dt

from django.core.files.base import ContentFile
from django.db import transaction
from djoser.serializers import UserCreateSerializer
from recipes.models import Follow, Ingredient, Recipe, RecipeIngredient, Tag
from rest_framework import serializers
from users.models import User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            timestamp = int(dt.datetime.now().timestamp() * 1000)
            data = ContentFile(
                base64.b64decode(imgstr),
                name=f'media/recipes/images/img{str(timestamp)}.{ext}')
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all())
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class UserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'first_name', 'last_name')


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')
        read_only_fields = ('email', 'id', 'username', 'first_name',
                            'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_anonymous:
            return Follow.objects.filter(user=user, following=obj).exists()
        return False


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(
        many=True,
        required=True,
        source='recipeingredient_set')
    author = UserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault())
    is_in_shopping_cart = serializers.ReadOnlyField(default=False)
    is_favorited = serializers.ReadOnlyField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        tags = representation.pop('tags')
        result = []
        for tag in tags:
            cur_tag = Tag.objects.get(pk=tag)
            result.append(
                {"id": cur_tag.id,
                 "name": cur_tag.name,
                 "color": cur_tag.color,
                 "slug": cur_tag.slug}
            )
        representation['tags'] = result
        return representation

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('recipeingredient_set')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        batch = []
        for ingredient in ingredients:
            batch.append(RecipeIngredient(
                recipe=recipe, **ingredient))
        RecipeIngredient.objects.bulk_create(batch)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('recipeingredient_set')
        tags = validated_data.pop('tags')
        recipe = instance
        recipe.tags.set(tags)
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        batch = []
        for ingredient in ingredients:
            batch.append(RecipeIngredient(
                recipe=recipe, **ingredient))
        RecipeIngredient.objects.bulk_create(batch)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.name = validated_data.get('name', recipe.name)
        recipe.cooking_time = validated_data.get(
            'cooking_time', recipe.cooking_time)
        recipe.image = validated_data.get('image', recipe.image)
        recipe.save()
        return recipe

    def validate_ingredients(self, ingredients):
        map = set()
        for obj in ingredients:
            if obj['ingredient'].pk in map:
                raise serializers.ValidationError(
                    'Ingredients cannot be the same')
            if obj['amount'] <= 0:
                raise serializers.ValidationError(
                    'Amount cannot be zero or less')
            map.add(obj['ingredient'].pk)
        return ingredients


class RecipeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')


class SubscriptionSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_anonymous:
            if Follow.objects.filter(user=user, following=obj).exists():
                return True
        return False

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        recipes = obj.recipes.all().order_by('-created_at', '-pk')
        query_params = self.context['request'].query_params
        if 'recipes_limit' in query_params:
            recipes_limit = int(query_params['recipes_limit'])
            recipes = recipes[:recipes_limit]
        serializer = RecipeShortSerializer(recipes, many=True)
        return serializer.data
