from rest_framework import viewsets
from foods.models import Tag, Recipe, Ingredient, Favorite, ShoppingCart
from users.models import User, Follow
from .serializers import UserFollowSerializer, TagSerializer, IngredientSerializer, RecipeSerializer, UserSerializer, UserPasswordSerializer
from rest_framework import mixins, status 
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


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

    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
    
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
        #permission_classes=[IsAuthenticated],
        #serializer_class=UserSerializer,
    )
    def get_followers(self, request):
        follow = Follow.objects.filter(user_id=self.request.user.id)
        following = User.objects.prefetch_related('follower').filter(
            following__in=follow.values('author_id'))
        serializer = UserSerializer(following, many=True)
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
            context = {'request': request}
            data = {'author': author.id,
                    'user': user.id}
            serializer = UserFollowSerializer(data=data) #, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        following = Follow.objects.get(author=author.id, user=user.id)
        following.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
