from rest_framework import viewsets
from foods.models import (
    Tag, Recipe, Ingredient, Favorite, ShoppingCart,
    IngredientRecipe,)
from users.models import User, Follow
from .serializers import (
    RecipePostSerializer, RecipeFORSerializer, UserFollowSerializer,
    TagSerializer, IngredientSerializer, RecipeSerializer,
    UserSerializer, UserPasswordSerializer)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Sum
from .permissions import IsAdminAuthorOrReadOnly
from .paginators import PageNumberPaginationWithLimit
from .filters import RecipeFilter


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Tag: только чтение."""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Ingredient: только чтение."""

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filterset_fields = ('name',)


class RecipesViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Recipes: чтение и запись."""

    serializer_class = RecipeSerializer
    permission_classes = [IsAdminAuthorOrReadOnly]
    pagination_class = PageNumberPaginationWithLimit
    http_method_names = ['get', 'post', 'patch', 'delete']
    filterset_class = (RecipeFilter)
    ordering_field = ('-pub_date',)

    def get_queryset(self):
        return Recipe.objects.add_anotations_recipe(self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['post', 'delete'],
        detail=False, url_path=r'(?P<recipe_id>\d+)/favorite',
        permission_classes=[IsAuthenticated],
        serializer_class=RecipeFORSerializer,
    )
    def favorite(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.method == 'POST':
            context = {'request': request,
                       'recipe_id': recipe_id,
                       'user_id': request.user.id,
                       'def': 'favorite'}
            serializer = RecipeFORSerializer(
                data=request.data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        favorite = get_object_or_404(Favorite, recipe=recipe.id, user=user.id)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['post', 'delete'],
        detail=False, url_path=r'(?P<recipe_id>\d+)/shopping_cart',
        permission_classes=[IsAuthenticated])
    def shopping(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.method == 'POST':
            context = {'request': request,
                       'recipe_id': recipe_id,
                       'user_id': request.user.id,
                       'def': 'shopping'}
            serializer = RecipeFORSerializer(
                data=request.data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        favorite = get_object_or_404(
           ShoppingCart, recipe=recipe.id, user=user.id)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get'],
        detail=False, url_path='download_shopping_cart',
        permission_classes=[IsAuthenticated])
    def download(self, request):
        filter = ShoppingCart.objects.filter(
            user_id=request.user.id).values_list('recipe_id')
        result = IngredientRecipe.objects.filter(
            recipe_id__in=filter).values_list(
                'ingredient__name', 'ingredient__measurement_unit')
        qs = result.annotate(Sum('amount'))
        text = ['Список покупок:']
        for ing in qs:
            ing = f'{ing[0]}, {ing[1]}: {ing[2]} '
            text.append(ing)
        text_file = '\n'.join(text)
        filename = 'shopping_cart.txt'
        response = HttpResponse(text_file, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return RecipePostSerializer
        return RecipeSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Users: чтение и запись."""

    serializer_class = UserSerializer
    http_method_names = ['post', 'get', 'delete']
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPaginationWithLimit

    def get_permissions(self):
        if self.action == 'create':
            return ((AllowAny(),))
        return super().get_permissions()

    def get_queryset(self):
        return User.objects.add_anotations_user(self.request.user.id)

    @action(
        methods=['get'],
        detail=False, url_path='me',
        serializer_class=UserSerializer,
    )
    def get_request_user(self, request):
        user = request.user
        user = User.objects.add_anotations_user(
            self.request.user.id).get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['post'],
        url_path='set_password',
        detail=False,
        serializer_class=UserPasswordSerializer,
        permission_classes=[AllowAny])
    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()
        return Response(
            'Пароль успешно изменен!', status=status.HTTP_204_NO_CONTENT
        )

    @action(
        methods=['get'],
        detail=False, url_path='subscriptions',
        serializer_class=UserFollowSerializer)
    def get_followers(self, request):
        follow_set = Follow.objects.filter(
            user_id=request.user.id).values_list('author')
        follow = User.objects.add_anotations_user(self.request.user.id).filter(
            id__in=[follow_set])
        if self.request.query_params.get('recipes_limit'):
            limit = self.request.query_params.get('recipes_limit')
            follow = follow.filter(recipes_limit=limit)
        serializer = UserFollowSerializer(follow, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['post', 'delete'],
        detail=False, url_path=r'(?P<author_id>\d+)/subscribe',
        # permission_classes=[IsAuthenticated],
        serializer_class=UserFollowSerializer,
    )
    def follow(self, request, author_id):
        user = request.user
        author = get_object_or_404(User, id=author_id)
        if request.method == 'POST':
            context = {
                'request': request,
                'author_id': author.id,
                'user_id': user.id
            }
            serializer = UserFollowSerializer(
                data=request.data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        following = get_object_or_404(Follow, author=author.id, user=user.id)
        following.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
