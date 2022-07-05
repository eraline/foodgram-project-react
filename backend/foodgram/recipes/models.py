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
    measurement_unit = models.CharField(max_length=200)


class Recipe(models.Model):
    name = models.CharField(max_length=200, unique=True)
    text = models.TextField()
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
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, db_index=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='one_uique_ingredient_per_recipe'
            )
        ]

class ShoppingCart(models.Model):
    user = models.ForeignKey(
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
    following = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following'
    )
