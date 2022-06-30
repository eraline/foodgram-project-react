from django.db import models

from users.models import User

class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True)
    color = models.CharField(max_length=7, null=True)
    slug = models.SlugField(null=True)

class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=200)


class Recipe(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    image =  models.ImageField()
    cooking_time = models.IntegerField()
    author = models.ForeignKey(User, 
        on_delete=models.CASCADE,
        related_name='recipes')
    tags = models.ManyToManyField(
        Tag,
        related_name='tags')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='ingredients')

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()

class ShoppingCart(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
        related_name='shopping_cart')

class Favourite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True
    )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favourites')

class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following'
    )
