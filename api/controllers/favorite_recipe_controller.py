
import traceback
from django.views.decorators.csrf import csrf_exempt

from api.decorators.decorators import auth_api
from api.controllers.classes.favorite_recipes import FavoriteRecipe
from api.exceptions.general_exception import GeneralException
from api.services.api_response import ApiResponse


@csrf_exempt
@auth_api
def add_recipe_to_fav(request):
    try:

        recipe = FavoriteRecipe(request)
        return recipe.add_recipe_to_fav()

    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)


@csrf_exempt
@auth_api
def get_fav_recipes(request):
    try:

        recipe = FavoriteRecipe(request)
        return recipe.get_fav_recipes()

    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)


@csrf_exempt
@auth_api
def get_favorite_recipe_details(request):
    try:

        recipe = FavoriteRecipe(request)
        return recipe.get_favorite_recipe_details()

    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)

@csrf_exempt
@auth_api
def delete_fav_recipe(request):
    try:

        recipe = FavoriteRecipe(request)
        return recipe.delete_fav_recipe()

    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)


