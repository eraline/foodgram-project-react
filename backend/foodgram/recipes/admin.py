from django.contrib import admin

from . import models

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit')

admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.Recipe)