import re

from django.core.exceptions import ValidationError
from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from foods.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                          ShoppingCart, Tag)
from rest_framework import serializers
from users.models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User:
    вывод основной информации о пользователе или создание нового.
    """

    is_subscribed = serializers.BooleanField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'password'
        )
        read_only_fields = ('id', 'is_subscribed')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate_username(self, username):
        pattern = re.compile(r'^[\w.@+-]+')

        if pattern.fullmatch(username) is None:
            match = re.split(pattern, username)
            symbol = ''.join(match)
            raise ValidationError(f'Некорректные символы в username: {symbol}')
        return username


class UserPasswordSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User: сброс пароля."""

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

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source='ingredient_id')
    name = serializers.StringRelatedField(source='ingredient.name')
    measurement_unit = serializers.StringRelatedField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientRecipePostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели IngredientRecipe:
    вложенный сериализатор (для создания рецепта).
    """

    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(write_only=True, min_value=1)

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
    ingredients = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    is_favorited = serializers.BooleanField()
    is_in_shopping_cart = serializers.BooleanField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'name', 'is_favorited',
            'is_in_shopping_cart', 'image', 'text', 'cooking_time'
        )
        read_only_fields = ('__all__',)

    def get_author(self, obj):
        qs = User.objects.add_anotations_user(
            self.context['request'].user.id).get(recipe__author=obj.author)
        return UserSerializer(qs).data

    def get_ingredients(self, obj):
        id_ingredients = IngredientRecipe.objects.filter(
            recipe=obj)
        return IngredientRecipeSerializer(id_ingredients, many=True).data


class RecipePostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe: создание и обновление."""

    ingredients = IngredientRecipePostSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'name',
                  'image', 'text', 'cooking_time')

    def ingredients_create(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_in_recipe = [
                IngredientRecipe(
                    ingredient=Ingredient.objects.get(id=ingredient['id']),
                    recipe=recipe,
                    amount=ingredient['amount'])
            ]
            IngredientRecipe.objects.bulk_create(ingredient_in_recipe)
        return None

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop('ingredients')
        tags_val = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe = Recipe.objects.add_anotations_recipe(
            self.context['request'].user.id).get(id=recipe.id)
        ingredients = self.initial_data.pop('ingredients')
        self.ingredients_create(ingredients, recipe)
        recipe.tags.set(tags_val)
        return recipe

    def update(self, instance, validated_data):
        validated_data.pop('ingredients')
        tags = validated_data.pop('tags')

        ingredients = self.initial_data.pop('ingredients', None)

        if tags is not None:
            tags = instance.tags.set(tags)

        if ingredients is not None:
            IngredientRecipe.objects.filter(recipe=instance).delete()
            self.ingredients_create(ingredients, instance)
        return super().update(instance, validated_data)

    def to_representation(self, value):
        return RecipeSerializer(value, context=self.context).data

    def validate_cooking_time(self, cooking_time):
        if cooking_time <= 0:
            raise ValidationError(
                'Время приготовления должно быть больше нуля.')
        return cooking_time

    def validate_ingredients(self, value):
        if len(value) < 1:
            raise serializers.ValidationError('Добавьте ингредиент!')
        return value


class RecipeFORSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe: вложенный сериализатор."""

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'image', 'cooking_time'
        )
        read_only_fields = ('__all__',)

    @transaction.atomic
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


class UserFollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User: вывод информации о подписках."""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source='recipes_limit', read_only=True)
    is_subscribed = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )
        read_only_fields = ('__all__',)

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj)
        return RecipeFORSerializer(recipes, many=True).data

    def create(self, validated_data):
        Follow.objects.create(
            author_id=self.context.get('author_id'),
            user_id=self.context.get('user_id'))
        return User.objects.add_anotations_user(
            self.context['request'].user.id).get(
                id=self.context.get('author_id'))

    def validate(self, data):
        if self.context['request'].method == 'POST' and Follow.objects.filter(
                user_id=self.context['request'].user.id,
                author_id=self.context.get('author_id')).exists():
            raise serializers.ValidationError('Вы уже подписаны!')

        if self.context['request'].user.id == self.context.get('author_id'):
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!')
        return data
