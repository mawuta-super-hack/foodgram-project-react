from django.db import models
from users.models import User


class Tag(models.Model):
    '''Модель для описания тегов'''
    name = models.CharField(
        verbose_name='Название', max_length=200, unique=True)
    color = models.CharField(
        verbose_name='Цвет', max_length=7, unique=True)
    slug = models.SlugField(
        verbose_name='Ссылка', max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название', max_length=200, unique=True)
    measurement_unit = models.CharField(
        verbose_name='Единица измерения', max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    '''Модель для описания рецептов'''
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор')
    name = models.CharField(verbose_name='Название', max_length=200)
    image = models.ImageField(
        verbose_name='Картинка',
        blank=False,
        upload_to='foods/'
    )
    text = models.TextField(verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientRecipe')
    tags = models.ManyToManyField(Tag, through='TagRecipe')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления', default=1)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    amount = models.IntegerField(
        verbose_name='Количество', default=1)

    def __str__(self):
        return f'{self.recipe}: {self.ingredient} '

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, verbose_name='Тег')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')

    def __str__(self):
        return f'{self.tag} {self.recipe}'

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Любимый рецепт')

    class Meta:
        verbose_name_plural = "Избранные рецепты"
        constraints = (models.UniqueConstraint(
            fields=['user', 'recipe'], name='unique_combination'),)


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopper',
        verbose_name='Покупатель')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_in_cart',
        verbose_name='Рецепт в списке покупок')

    class Meta:
        verbose_name_plural = "Список покупок"
        constraints = (models.UniqueConstraint(
            fields=['user', 'recipe'], name='unique_combination'),)
