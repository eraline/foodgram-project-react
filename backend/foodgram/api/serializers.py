from dataclasses import fields
from rest_framework import serializers

from recipes.models import Tag, Recipe, Ingredient, RecipeIngredient

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class RecipeIngredientSerializer(serializers.ModelSerializer):
    # id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    unit = serializers.ReadOnlyField(source='ingredient.unit')
    class Meta:
        model = RecipeIngredient
        fields = ('name', 'unit', 'amount')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__' 

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True, required=False)
    # tags = TagSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        # tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        # for tag in tags:
        #     cur_tag, status = Tag.objects.get_or_create(**tag)
        #     recipe.tags.add(cur_tag)
        for ingredient in ingredients:
            amount = ingredient.pop('amount')
            cur_ingredient = Ingredient.objects.get_or_create(**ingredient)
            RecipeIngredient.objects.get_or_create(recipe=recipe, amount=amount, **ingredient)
        return recipe

