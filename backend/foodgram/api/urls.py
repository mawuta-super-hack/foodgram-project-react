from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TagsViewSet, RecipesViewSet, IngredientsViewSet, UsersViewSet)

router_v1 = DefaultRouter()
router_v1.register(r'users', UsersViewSet, basename='users')
router_v1.register(r'tags', TagsViewSet, basename='tags')
router_v1.register(r'recipes', RecipesViewSet, basename='recipes')
router_v1.register(r'ingredients', IngredientsViewSet, basename='ingredients')

urlpatterns = [

    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken'))
]
