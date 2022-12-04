from rest_framework import viewsets
from foods.models import Tag, Recipe, Ingredient, Favorite, ShoppingCart, IngredientRecipe
from users.models import User, Follow
from .serializers import IngredientRecipeSerializer, RecipePostSerializer, RecipeFORSerializer, ShoppingCartSerializer, UserFollowSerializer, TagSerializer, IngredientSerializer, RecipeSerializer, UserSerializer, UserPasswordSerializer
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Subquery, Sum 

class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Tag"""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для модели Ingredient"""

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipesViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Recipes"""
    
    ACTIONS = ['create', 'partial_update']
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['post', 'delete'],
        detail=False, url_path=r'(?P<recipe_id>\d+)/favorite',
        #permission_classes=[IsAuthenticated],
        serializer_class=RecipeFORSerializer,
    )
    def favorite(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.method == 'POST':
            context = {'request': request,
                        'recipe_id': recipe.id,
                        'user_id': user.id,
                        'def': 'favorite'}
            serializer = RecipeFORSerializer(data=request.data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        favorite = get_object_or_404(Favorite, recipe=recipe.id, user=user.id)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(
        methods=['post', 'delete'],
        detail=False, url_path=r'(?P<recipe_id>\d+)/shopping_cart',
        #permission_classes=[IsAuthenticated],
        serializer_class=ShoppingCartSerializer,
    )
    def shopping(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if request.method == 'POST':
            context = {'request': request,
                        'recipe_id': recipe.id,
                        'user_id': user.id,
                        'def': 'shopping'}
            serializer = RecipeFORSerializer(data=request.data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        favorite = get_object_or_404(ShoppingCart, recipe=recipe.id, user=user.id)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(
        methods=['get'],
        detail=False, url_path='download_shopping_cart',
        #permission_classes=[IsAuthenticated],
        #serializer_class=ShoppingCartSerializer,
    )
    def download(self, request):
        
        #FilePointer = open(file_path,"r")
        queryset = ShoppingCart.objects.filter(user_id=request.user.id).values_list('recipe_id')
        print(queryset)
        result = IngredientRecipe.objects.filter(
            recipe_id__in=queryset).values_list('ingredient__name', 'ingredient__measurement_unit')
        for_file = result.annotate(Sum('amount'))
        print(for_file)
        
        #serializer = IngredientRecipeSerializer(qs, many=True)open(for_file.file.path,"r"),
        response = HttpResponse(content_type='text/plain')#'"application/txt"; charset=UTF-8')
        response['Content-Disposition'] = 'attachment; filename=Shopep.txt'#            "  %s"' % filename)'attachment; filename={0}'.format(filename))
        response.write('список покупок ')
        response.write(list(for_file))
        return response
    
        #file_path = file_url
        #FilePointer = open(file_path,"r")
        #response = HttpResponse(FilePointer,content_type='application/msword')
        #response['Content-Disposition'] = 'attachment; filename=NameOfFile'

        #return response.


    #def download(self, *args, **kwargs):
        #instance = self.get_object()

        # get an open file handle (I'm just using a file attached to the model for this example):
        #file_handle = instance.file.open()

        # send file
        #response = FileResponse(file_handle, content_type='"application/pdf"; charset=UTF-8'')
        #response['Content-Length'] = instance.file.size
        #response['Content-Disposition'] = 'attachment; filename="%s"' % filename

        #return response

    def get_serializer_class(self):
        if self.action in self.ACTIONS:
            return RecipePostSerializer
        return RecipeSerializer

    #ACTIONS = ['create', 'partial_update']
    #serializer_class = TitlePostSerializer
    #queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    #filterset_class = TitleFilter
    #permission_classes = [IsAdminOrReadOnly]
    #ordering_field = ('name',)


class CreateListRetrieveViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                   mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class UsersViewSet(CreateListRetrieveViewSet):
    """Вьюсет для модели Users"""

    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(
        methods=['get'],
        detail=False, url_path='me',
        #permission_classes=[IsAuthenticated],
        serializer_class=UserSerializer,
    )
    def get_request_user(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        #if request.method == 'GET':
        #    serializer = self.get_serializer(
        #        user, data=request.data, partial=True
        #    )
        #    serializer.is_valid(raise_exception=True)
        #    serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

        #@action(["get", "put", "patch", "delete"], detail=False)
        #def me(self, request, *args, **kwargs):
        #self.get_object = self.get_instance
        #return self.retrieve(request, *args, **kwargs)
    
    @action(methods=['post'],  url_path='set_password', detail=False, serializer_class=UserPasswordSerializer) 
        #serializer_class=UserSerializer)
    #def set_password(self, request):
    #    pass
        #чото дописать + сериализер
    #@action(["post"], detail=False)
    def get_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(
        methods=['get'],
        detail=False, url_path='subscriptions',
        permission_classes=[IsAuthenticated],
        serializer_class=UserFollowSerializer
    )
    def get_followers(self, request):
        if request.user:
            follow_set = Follow.objects.filter(
                user_id=request.user.id).values_list('author')
            follow = User.objects.filter(
                id__in=[follow_set])
            serializer = UserFollowSerializer(follow, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['post', 'delete'],
        detail=False, url_path=r'(?P<author_id>\d+)/subscribe',
        #permission_classes=[IsAuthenticated],
        #serializer_class=UserFollowSerializer,
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
