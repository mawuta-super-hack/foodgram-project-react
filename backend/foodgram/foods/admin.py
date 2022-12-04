from django.contrib import admin

from .models import (
    Recipe, Ingredient, Tag, Favorite, ShoppingCart, IngredientRecipe)
# TagRecipe,IngredientRecipe


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'measurement_unit')
    list_filter = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    search_fields = ('name',)


class TagRecipeline(admin.TabularInline):
    model = Recipe.tags.through


class IngredientRecipeline(admin.TabularInline):
    model = Recipe.ingredients.through


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'amount')
    list_filter = ('amount',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'author',)
    search_fields = ('name', 'description',)
    list_filter = ('name', 'author', 'tags',)
    empty_value_display = '-не указано-'
    inlines = (TagRecipeline, IngredientRecipeline)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
# Модель рецептов:
# На странице рецепта вывести общее число добавлений этого рецепта в избранное.
