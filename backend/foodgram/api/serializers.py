from dataclasses import fields
from rest_framework import serializers

from recipes.models import Tag, Recipe, Ingredient, RecipeIngredient

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ('ingredient','amount')


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
            RecipeIngredient.objects.get_or_create(recipe=recipe, **ingredient)
        return recipe
