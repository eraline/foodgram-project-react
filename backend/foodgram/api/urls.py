from email.mime import base
from rest_framework import routers
from api import views
from django.urls import include, path


router = routers.DefaultRouter()
router.register(r'tags', views.TagViewSet)
router.register(r'recipes', views.RecipeViewSet, basename='recipes')
router.register(r'ingredient', views.IngredientViewSet)
router.register(r'users', views.UserViewSet)
# router.register(r'recipe/(?P<recipe_id>\d+)/favourite',
#     views.FavouritesViewSet, basename='favourites')


urlpatterns = [
    path('', include(router.urls)),
    # path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # path('users/<int:user_id>/follow/',
    #     views.FollowingViewSet.as_view({'post':'create', 'delete':'perform_destroy'}),
    #     name='following')
    # path('recipe/<int:recipe_id>/favourite', views.FavouritesViewSet, name='favourite'),
    # path('recipe/(?P<recipe_id>\d+)/favourite',
    #     views.FavouritesViewSet)
]
