from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from api.controllers import auth_controller, recipe_controller, favorite_recipe_controller


urlpatterns = [
    # User Urls
    path('register/', auth_controller.register_user),
    path('login/', auth_controller.login_user),
    path('logout/', auth_controller.logout_user),
    path('update-password/', auth_controller.reset_password),
    path('update-profile/', auth_controller.edit_profile),
    path('user/', auth_controller.get_user_profile),
    path('delete-user/', auth_controller.delete_user),
    path('users/', auth_controller.user_listing),
    path('search-user/', auth_controller.search_user),

    # Recipe URLs
    path('recipes/', recipe_controller.get_recipes_by_user),
    path('add-recipe/', recipe_controller.add_recipe),
    path('get-recipe-details/', recipe_controller.get_recipe_by_id),
    path('get-recipe-listing/', recipe_controller.get_recipes_listing),
    path('delete-recipe/', recipe_controller.delete_recipe),
    path('edit-recipe/', recipe_controller.edit_recipe),
    path('search-recipe/', recipe_controller.search_recipe),

    # Favorite URLs
    path('add-to-favorite/', favorite_recipe_controller.add_recipe_to_fav),
    path('favorite-recipes/', favorite_recipe_controller.get_fav_recipes),
    path('get-favorite-recipe-details/', favorite_recipe_controller.get_favorite_recipe_details),
    path('remove-from-favorite/', favorite_recipe_controller.delete_fav_recipe),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)