from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                     ShoppingCart, Tag)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'color')
    search_fields = ('name', 'slug')


class TagRecipeline(admin.TabularInline):
    model = Recipe.tags.through
    min_num = 1
    extra = 0


class IngredientRecipeline(admin.TabularInline):
    model = Recipe.ingredients.through
    min_num = 1
    extra = 0


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'amount')
    list_filter = ('amount',)


class RecipeAdmin(admin.ModelAdmin):

    def add_favorite(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    add_favorite.short_description = 'Количество добавлений в избранное'
    list_display = ('id', 'name', 'author', 'pub_date', 'add_favorite')
    search_fields = ('name', 'description',)
    list_filter = ('name', 'author', 'tags',)
    empty_value_display = '-не указано-'
    inlines = (TagRecipeline, IngredientRecipeline)
    readonly_fields = ('add_favorite',)


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
