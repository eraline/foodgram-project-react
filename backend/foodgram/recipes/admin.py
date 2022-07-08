from django.contrib import admin
from users.models import User

from . import models


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)


class RecipeIngredientInline(admin.TabularInline):
    model = models.RecipeIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_filter = ('author', 'name', 'tags',)
    list_display = ('pk', 'author', 'name', 'text', 'favourites_count')
    readonly_fields = ('favourites_count',)

    def favourites_count(self, object):
        return models.Favourite.objects.filter(recipe=object).count()


class UserAdmin(admin.ModelAdmin):
    list_filter = ('first_name', 'username', 'email',)


admin.site.register(models.Tag)
admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.Favourite)
admin.site.register(models.ShoppingCart)
admin.site.register(models.Follow)
admin.site.register(User, UserAdmin)
