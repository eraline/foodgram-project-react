# Generated by Django 3.2 on 2022-07-14 12:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0007_auto_20220705_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='following',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='Following'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='Follower'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(max_length=200, verbose_name='Measurement unit'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Ingredien name'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Author of recipe'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Cooking time'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Recipe Name'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.FloatField(verbose_name='Quantity'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Shopping cart owner'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, null=True, verbose_name='Colour in HEX format'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Tag name'),
        ),
        migrations.AddConstraint(
            model_name='favourite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_recipe_per_favourites'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'following'), name='unique_user_following'),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_recipe_per_cart'),
        ),
    ]
