from rest_framework import serializers
from foods.models import Tag, Ingredient, Recipe, Favorite, ShoppingCart, IngredientRecipe
from users.models import User, Follow


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""
    
       
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name') #, 'is_subscrubed')


class UserFollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""
    #author_id = UserSerializer


    class Meta:
        model = Follow
        fields = ('author','user') #, 'is_subscrubed')


class UserPasswordSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""
    current_password = serializers.CharField(
        source='password')
    new_password = serializers.CharField()
    
    class Meta:
        model = User
        fields = ('new_password', 'current_password')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tag"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)

class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient"""
    #amount = serializers.SlugRelatedField(
    #    queryset=IngredientRecipeAmount.objects.filter(id_ingredient_recipe_id=), slug_field='amount'
    #)

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe"""

    tags = TagSerializer
    # author  сериализер  users
    ingredients = IngredientRecipeSerializer
    # is favorited
    # is in shop cart

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'ingredients', 'author', 'name',
                  'image', 'text', 'cooking_time')

        read_only_fields = ('id', 'tags', 'ingredients', 'author', 'name',
                            'image', 'text', 'cooking_time')
