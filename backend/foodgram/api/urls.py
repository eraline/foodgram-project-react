from rest_framework import routers
from api import views
from django.urls import include, path


router = routers.DefaultRouter()
router.register(r'tags', views.TagViewSet)
router.register(r'recipe', views.RecipeViewSet)
router.register(r'ingredient', views.IngredientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
