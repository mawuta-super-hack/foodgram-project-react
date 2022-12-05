from rest_framework import serializers
from foods.models import (
    Tag, Ingredient, Recipe, Favorite,
    ShoppingCart, IngredientRecipe, TagRecipe
    )
from users.models import User, Follow
from drf_extra_fields.fields import Base64ImageField
from django.db.models import Count, Subquery
import re
from django.core.exceptions import ValidationError
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User:
    вывод основной информации о пользователе или создание нового.
    """

    is_subscribed = serializers.BooleanField() # serializers.SerializerMetho
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'password'
        )
        read_only = ('id', 'is_subscribed')

    # def get_is_subscribed(self, obj):

    #    if Follow.objects.filter(
    #        user_id=self.context.get('request').user.id, author_id=obj.id
    #    ).exists():
    #        obj.is_subscribed = True
    #        return obj.is_subscribed
    #    obj.is_subscribed = False
    #    return obj.is_subscribed

    def validate_username(self, username):
        pattern = re.compile(r'^[\w.@+-]+')

        if pattern.fullmatch(username) is None:
            match = re.split(pattern, username)
            symbol = ''.join(match)
            raise ValidationError(f'Некорректные символы в username: {symbol}')
        return username


class UserPasswordSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User: сброс пароля.
    """

    current_password = serializers.CharField(
        source='password')
    new_password = serializers.CharField()

    class Meta:
        model = User
        fields = ('new_password', 'current_password')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag: вывод информации."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('name', 'color', 'slug')

    def validate_slug(self, slug):
        pattern = re.compile(r'^[-a-zA-Z0-9_]+$')

        if pattern.fullmatch(slug) is None:
            match = re.split(pattern, slug)
            symbol = ''.join(match)
            raise ValidationError(f'Некорректные символы в slug: {symbol}')
        return slug


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient: вывод информации."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели IngredientRecipe: вложенный сериализатор."""

    #id = serializers.SerializerMethodField()
    #name = serializers.SerializerMethodField()
    #measurement_unit = serializers.SerializerMethodField()

    # amount = serializers.SerializerMethodField()
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all(), source='ingredient_id')
    name = serializers.StringRelatedField(source='ingredient.name') 
    measurement_unit = serializers.StringRelatedField(source='ingredient.measurement_unit') 
    #amount = serializers.ImageField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')
        #read_only_fields = ('name', 'measurement_unit')

    #def get_id(self, obj):
    #    ob = Ingredient.objects.get(id=obj.ingredient_id)
    #    print(ob)
    #    return str(ob.id)

    #def get_name(self, obj):
    #    ob = Ingredient.objects.get(id=obj.ingredient_id)
    #    return ob.name

    #def get_measurement_unit(self, obj):
    #    ob = Ingredient.objects.get(id=obj.ingredient_id)
    #    return ob.measurement_unit


class IngredientRecipePostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели IngredientRecipe:
    вложенный сериализатор (для создания рецепта).
    """

    id = serializers.PrimaryKeyRelatedField(source='ingredient',
        queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(write_only=True, min_value=1)#SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')

    def get_amount(self, obj):
        amount = IngredientRecipe.objects.filter(
            ingredient=obj).values_list('amount', flat=True)
        return amount[0]


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe: вывод информации."""

    tags = TagSerializer(many=True)
    ingredients =  serializers.SerializerMethodField() # (many=True)
    author = serializers.SerializerMethodField()
    is_favorited = serializers.BooleanField() # serializers.SerializerMethodField()# is favorited
    is_in_shopping_cart = serializers.BooleanField() # serializers.SerializerMethodField()# is in shop cart

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',  'name', 'is_favorited',
            'is_in_shopping_cart', 'image', 'text', 'cooking_time'
        )
        read_only_fields = ['__all__']


    def get_author(self, obj):
        qs = User.objects.add_anotations_user(
            self.context['request'].user.id).get(recipe__author=obj.author)
        return UserSerializer(qs).data 
        
    # def get_is_favorited(self, obj):context['request'].user.id

    #    if Favorite.objects.filter(
    #        user_id=self.context.get('request').user.id, recipe_id=obj.id
    #    ).exists():
    #        obj.is_subscribed = True
    #        return obj.is_subscribed
    #    obj.is_subscribed = False
    #    return obj.is_subscribed

    # def get_is_in_shopping_cart(self, obj):

    #    if ShoppingCart.objects.filter(
    #        user_id=self.context.get('request').user.id, recipe_id=obj.id
    #    ).exists():
    #        obj.is_subscribed = True
    #        return obj.is_subscribed
    #    obj.is_subscribed = False
    #    return obj.is_subscribed

    def get_ingredients(self, obj):
        id_ingredients = IngredientRecipe.objects.filter(
            recipe=obj)#.values_list('id', flat=True)

        #id_ingredients_list = IngredientRecipe.objects.filter(
        #    recipe=obj).values_list('ingredient', flat=True)
        #ing_ser = Ingredient.objects.filter(id__in=[id_ingredients_list])

        # an = ing_ser.annotate(
        #    amount=Subquery(IngredientRecipe.objects.filter(id__in=[id_ir]).values_list('amount')))
        return IngredientRecipeSerializer(id_ingredients, many=True).data
# ###   вот тут странно работает, зачем строки 180т182 если передается 177


class RecipePostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe: создание и обновление."""

    ingredients = IngredientRecipePostSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()) #, slug_field='id')
    image = Base64ImageField()
    #is_favorited = serializers.BooleanField(read_only=True)
    #is_in_shopping_cart = serializers.BooleanField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'name',
                  'image', 'text', 'cooking_time')

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop('ingredients')
        tags_val = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe = Recipe.objects.add_anotations_recipe(
            self.context['request'].user.id).get(id=recipe.id)
        ing_in = self.initial_data.pop('ingredients')
        for ing in ing_in:
            ing_rec = [
                IngredientRecipe(
                    ingredient=Ingredient.objects.get(id=ing['id']),
                    recipe=recipe,
                    amount=ing['amount'])
            ]
            IngredientRecipe.objects.bulk_create(ing_rec)
        for tg in tags_val:
            tags = [TagRecipe(tag=tg, recipe=recipe)]
            TagRecipe.objects.bulk_create(tags)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        Recipe.objects.filter(
            id=instance.id).update(
                name=validated_data['name'],
                image=validated_data['image'],
                text=validated_data['text'],
                cooking_time=validated_data['cooking_time'])
        recipe = Recipe.objects.add_anotations_recipe(
            self.context['request'].user.id).get(id=instance.id)

        ingredients = self.initial_data.pop('ingredients', None)
        tags = self.validated_data.pop('tags', None)

        if tags is not None:
            TagRecipe.objects.filter(recipe=recipe).delete()
            for tg in tags:
                tag = [TagRecipe(tag=tg, recipe=recipe)]
                TagRecipe.objects.bulk_create(tag)

        if ingredients is not None:
            IngredientRecipe.objects.filter(recipe=recipe).delete()
            
            for ing in ingredients:
                ing_rec = [
                    IngredientRecipe(
                        ingredient=Ingredient.objects.get(id=ing['id']),
                        recipe=recipe,
                        amount=ing['amount'])
                ]
                IngredientRecipe.objects.bulk_create(ing_rec)
        return recipe

    # def update(self, instance, validated_data):
    #    if 'tags' in self.validated_data:
    #        tags_data = validated_data.pop('tags')
    #        instance.tags.set(tags_data)
    #    if 'ingredients' in self.validated_data:
    #        ingredients_data = validated_data.pop('ingredients')
    #        amount_set = IngredientRecipe.objects.filter(
    #            recipe__id=instance.id)
    #        amount_set.delete()
    #        IngredientRecipe.objects.create(
    #            ingredients_data,
    #            instance
    #        )
    #    return super().update(instance, validated_data)

    def to_representation(self, value):
        return RecipeSerializer(value, context=self.context).data

    def validate_cooking_time(self, cooking_time):
        if cooking_time <= 0:
            raise ValidationError(
                'Время приготовления должно быть больше нуля.')
        return cooking_time

#class FavoriteRecipeSerializer(serializers.ModelSerializer):

#    class Meta:
#        model = Favorite
#        fields = ('user', 'recipe',)#('id', 'name', 'image', 'cooking_time')


#class ShoppingCartSerializer(serializers.ModelSerializer):

#    class Meta:
#        model = ShoppingCart
#       fields = ('user', 'recipe')#('id', 'name', 'image', 'cooking_time')


class RecipeFORSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe: вложенный сериализатор."""

    class Meta:
        model = Recipe
        fields = (
            'id',  'name', 'image', 'cooking_time'
        )
        read_only_fields = (
            'id',  'name', 'image', 'cooking_time'
        )

    def create(self, validated_data):
        if self.context.get('def') == 'favorite':
            Favorite.objects.create(
                recipe_id=self.context.get('recipe_id'),
                user_id=self.context.get('user_id'))
            return Recipe.objects.get(id=self.context.get('recipe_id'))
        ShoppingCart.objects.create(
                recipe_id=self.context.get('recipe_id'),
                user_id=self.context.get('user_id'))
        return Recipe.objects.get(id=self.context.get('recipe_id'))
#add_anotations_recipe(
 #           self.context['request'].user.id)

class UserFollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User: вывод информации о подписках."""

    recipes = serializers.SerializerMethodField()
    # recipes_count = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(source='recipes_limit', read_only=True)
    is_subscribed = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )
        read_only_fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        return RecipeFORSerializer(recipes, many=True).data

    # def get_recipes_count(self, obj):
    #    recipes_count = Recipe.objects.filter(author=obj.id).count()
    #    return recipes_count

    # def get_is_subscribed(self, obj):
    #    print(self.context)
    #    if Follow.objects.filter(
    #        author_id=obj
    #    ).exists():
    #        obj.is_subscribed = True
    #        return obj.is_subscribed
    #    obj.is_subscribed = False
    #    return obj.is_subscribed

    def create(self, validated_data):
        Follow.objects.create(
            author_id=self.context.get('author_id'),
            user_id=self.context.get('user_id'))
        return User.objects.add_anotations_user(
            self.context['request'].user.id).get(id=self.context.get('author_id'))

    def validate(self, data):
        if self.context['request'].method == 'POST':
            obj = Follow.objects.filter(
                user_id=self.context['request'].user.id,
                author_id=self.context.get('author_id')).exists()
            if obj is True:
                raise serializers.ValidationError(
                    'Вы уже подписаны!')

        if self.context['request'].user.id == self.context.get('author_id'):
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!')
        return data
