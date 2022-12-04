from rest_framework import serializers
from foods.models import Tag, Ingredient, Recipe, Favorite, ShoppingCart, IngredientRecipe, TagRecipe
from users.models import User, Follow
from drf_extra_fields.fields import Base64ImageField
from django.db.models import Count, Subquery

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""
    is_subscribed = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'password'
        )
        read_only = ('id', 'is_subscribed')
        

    def get_is_subscribed(self, obj):
    
        if Follow.objects.filter(
            user_id=self.context.get('request').user.id, author_id=obj.id
        ).exists():
            obj.is_subscribed = True
            return obj.is_subscribed
        obj.is_subscribed = False
        return obj.is_subscribed


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
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient"""
    id =serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()
    
    #amount = serializers.SerializerMethodField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount' )
        read_only_fields = ('name', 'measurement_unit')
    
    def get_id(self, obj):
        print(obj.__dict__)
        ob = Ingredient.objects.get(id=obj.ingredient_id)
        print(ob)
        return str(ob.id)
    
    def get_name(self, obj):
        ob = Ingredient.objects.get(id=obj.ingredient_id)
        return ob.name

    def get_measurement_unit(self, obj):
        ob = Ingredient.objects.get(id=obj.ingredient_id)
        return ob.measurement_unit



class IngredientRecipePostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredient"""
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all())
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('id', 'amount')

    def get_amount(self, obj):
        amount = IngredientRecipe.objects.filter(
            ingredient=obj).values_list('amount', flat=True)
        return amount[0]

class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe"""

    tags = TagSerializer(many=True)
    ingredients =  serializers.SerializerMethodField()#(many=True)
    author = UserSerializer()
    is_favorite = serializers.SerializerMethodField()# is favorited
    is_in_shopping_cart = serializers.SerializerMethodField()# is in shop cart

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',  'name', 'is_favorite',
            'is_in_shopping_cart', 'image', 'text', 'cooking_time'
        )
        read_only_fields = ['__all__']

    def get_is_favorite(self, obj):

        if Favorite.objects.filter(
            user_id=self.context.get('request').user.id, recipe_id=obj.id
        ).exists():
            obj.is_subscribed = True
            return obj.is_subscribed
        obj.is_subscribed = False
        return obj.is_subscribed

    def get_is_in_shopping_cart(self, obj):

        if ShoppingCart.objects.filter(
            user_id=self.context.get('request').user.id, recipe_id=obj.id
        ).exists():
            obj.is_subscribed = True
            return obj.is_subscribed
        obj.is_subscribed = False
        return obj.is_subscribed

    def get_ingredients(self, obj):
        id_ir = IngredientRecipe.objects.filter(recipe=obj)#.values_list(
        #   'id', flat=True)
        id_ingr = IngredientRecipe.objects.filter(recipe=obj).values_list(
           'ingredient', flat=True)
        print(id_ingr, id_ir)
        ing_ser = Ingredient.objects.filter(id__in=[id_ingr])
        print('ing_ser', ing_ser)
        #an = ing_ser.annotate(
        #    amount=Subquery(IngredientRecipe.objects.filter(id__in=[id_ir]).values_list('amount')))
        print('an\\', 1)

        return IngredientRecipeSerializer(id_ir, many=True).data



class RecipePostSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe"""

    ingredients = IngredientRecipePostSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(many=True,
        queryset=Tag.objects.all())#, slug_field='id')
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'name',
                  'image', 'text', 'cooking_time')

    def create(self, validated_data):
        validated_data.pop('ingredients')
        tags_val = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

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

    def update(self, instance, validated_data):
        Recipe.objects.filter(
            id=instance.id).update(
                name=validated_data['name'],
                image=validated_data['image'],
                text=validated_data['text'],
                cooking_time=validated_data['cooking_time'])
        recipe = Recipe.objects.get(id=instance.id)
        ing_in = self.initial_data.pop('ingredients')
        tags_val = validated_data.pop('tags')
        IngredientRecipe.objects.filter(recipe=recipe).delete() 
        TagRecipe.objects.filter(recipe=recipe).delete()
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

    #def update(self, instance, validated_data):
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



class FavoriteRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ('user', 'recipe',)#('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')#('id', 'name', 'image', 'cooking_time')


class RecipeFORSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipe"""
    
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
        

class UserFollowSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""
    
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

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

    def get_recipes_count(self, obj):
        recipes_count = Recipe.objects.filter(author=obj.id).count()
        return recipes_count

    def get_is_subscribed(self, obj):
        print(self.context)
        if Follow.objects.filter(
            author_id=obj
        ).exists():
            obj.is_subscribed = True
            return obj.is_subscribed
        obj.is_subscribed = False
        return obj.is_subscribed

    def create(self, validated_data):
        Follow.objects.create(
            author_id=self.context.get('author_id'),
            user_id=self.context.get('user_id'))
        return User.objects.get(id=self.context.get('author_id'))
