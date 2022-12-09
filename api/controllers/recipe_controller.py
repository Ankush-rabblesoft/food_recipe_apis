
import traceback
from django.views.decorators.csrf import csrf_exempt

from api.decorators.decorators import auth_api
from api.controllers.classes.recipe import Recipes
from api.exceptions.general_exception import GeneralException
from api.services.api_response import ApiResponse


@csrf_exempt
@auth_api
def get_recipes_by_user(request):
    try:
        recipe = Recipes(request)
        return recipe.get_recipes()

    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)

@csrf_exempt
@auth_api
def add_recipe(request):
    try:
        recipe = Recipes(request)
        return recipe.add_recipe()

    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)

@csrf_exempt
@auth_api
def get_recipe_by_id(request):
    try:
        recipe = Recipes(request)
        return recipe.get_recipe_details()

    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)

@csrf_exempt
@auth_api
def get_recipes_listing(request):
    try:
        recipe = Recipes(request)
        return recipe.recipes_listing()

    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)

@csrf_exempt
@auth_api
def delete_recipe(request):
    try:
        recipe = Recipes(request)
        return recipe.delete_recipe()

    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)

@csrf_exempt
@auth_api
def edit_recipe(request):
    try:
        recipe = Recipes(request)
        return recipe.update_recipe()

    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)

@csrf_exempt
@auth_api
def search_recipe(request):
    try:
        recipe = Recipes(request)
        return recipe.search_recipe()

    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)
