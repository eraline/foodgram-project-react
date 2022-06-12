from dataclasses import fields
from email.policy import default
from rest_framework import serializers

from recipes.models import Tag, Recipe, Ingredient, RecipeIngredient, User

class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = '__all__'

class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    unit = serializers.ReadOnlyField(source='ingredient.unit')
    class Meta:
        model = RecipeIngredient
        fields = ('ingredient','name', 'amount','unit')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')
        read_only_fields = ('email', 'id', 'username', 'first_name', 'last_name')

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__' 

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(
        many=True, 
        required=False, 
        source='recipeingredient_set')
    author = UserSerializer(
        read_only=True, 
        default=serializers.CurrentUserDefault())
    class Meta:
        model = Recipe
        fields = '__all__'
# 
    def create(self, validated_data):
        ingredients = validated_data.pop('recipeingredient_set')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            amount = ingredient.pop('amount')
            RecipeIngredient.objects.get_or_create(recipe=recipe, amount=amount, **ingredient)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('recipeingredient_set')
        tags = validated_data.pop('tags')
        recipe = instance
        # recipe = Recipe.objects.get(**validated_data)
        recipe.tags.set(tags)
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        for ingredient in ingredients:
            amount = ingredient.pop('amount')
            RecipeIngredient.objects.get_or_create(recipe=recipe, amount=amount, **ingredient)
        return recipe

