from api import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'tags', views.TagViewSet)
router.register(r'recipes', views.RecipeViewSet, basename='recipes')
router.register(r'ingredients', views.IngredientViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
