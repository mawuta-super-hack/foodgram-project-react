from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (TagsViewSet, RecipesViewSet, IngredientsViewSet, UsersViewSet) 

router_v1 = DefaultRouter()
router_v1.register(r'users', UsersViewSet, basename='users')
#router_v1.register(r'users/me')
#router_v1.register(r'users/set_password', )
#router_v1.register = (r'auth/token/login')
#router_v1.register = (r'auth/token/logout')
#router_v1.register = (r'recipes/download_shopping_cart/')
#router_v1.register = (r'recipes/id/download_shopping_cart/')
# тут еще с ид внутри есть пост и дел
#router_v1.register = (r'recipes/id/favorite')
#router_v1.register = (r'users/subscriptions/')
#router_v1.register = (r'users/id/subscribe')

router_v1.register(r'tags', TagsViewSet, basename='tags')
router_v1.register(r'recipes', RecipesViewSet, basename='recipes')
router_v1.register(r'ingredients', IngredientsViewSet, basename='ingredients')
#router_v1.register(r'/users/(?P<user_id>\d+)/subscribe', FollowViewSet, basename='follow')

urlpatterns = [
    
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
   # path('users/set_password/', set_password, name='set_password'),
    #path('v1/auth/', include(urlpatterns_auth)),
]