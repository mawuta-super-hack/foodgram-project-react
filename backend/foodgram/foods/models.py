from django.db import models
from users.models import User
from django.db.models import OuterRef, Exists


class Tag(models.Model):
    """Модель для описания тегов."""

    name = models.CharField(
        verbose_name='Название', max_length=200)
    color = models.CharField(
        verbose_name='Цвет', max_length=7)
    slug = models.SlugField(
        verbose_name='Ссылка', max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель для описания ингредиентов."""

    name = models.CharField(
        verbose_name='Название', max_length=200)
    measurement_unit = models.CharField(
        verbose_name='Единица измерения', max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class RecipeQuerySet(models.QuerySet):
    """Аннотация дополнительных полей для рецептов."""

    def add_anotations_recipe(self, user_id):
        return Recipe.objects.annotate(
            is_favorited=Exists(
                Favorite.objects.filter(
                    user_id=user_id, recipe__id=OuterRef('id')
                ))
            ).annotate(
            is_in_shopping_cart=Exists(
                ShoppingCart.objects.filter(
                    user_id=user_id, recipe__id=OuterRef('id'))))


class Recipe(models.Model):
    """Модель для описания рецептов."""

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
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

    objects = RecipeQuerySet.as_manager()


class IngredientRecipe(models.Model):
    """Связующая модель: рецепты и ингредиенты."""

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
    """Связующая модель: рецепты и теги."""

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
    """Вспомогательная модель: добавление рецепта в избранное."""

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
    """Вспомогательная модель: добавление рецепта в корзину."""

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
