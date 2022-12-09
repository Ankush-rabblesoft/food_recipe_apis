
import re

from api.exceptions.general_exception import GeneralException
from api.models import Favorite, Recipe, Ingredient
from api.services.api_response import ApiResponse
from api.services.token_service import TokenService


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

class FavoriteRecipe():

    request = None
    token_service = None

    def __init__(self, request):

        self.request = request
        self.token_service = TokenService()
    
    def add_recipe_to_fav(self):
        request = self.request

        request_data = request.json

        if not request_data:
            raise GeneralException("Request data not valid")

        if not request.method=="POST":
            raise GeneralException("Request method should be POST")

        token = self.token_service.get_token_from_request(request)
        
        if not token:
            return ApiResponse.general_error(message="Not a valid token")
        
        user = self.token_service.get_user_from_token(token)        
        
        if not user:
            raise GeneralException('User not found')

        recipe_id = request_data.get('recipe_id')
        
        recipe = Recipe.objects.filter(id=recipe_id).first()

        if not recipe:
            return ApiResponse.general_error(message="Recipe not found with the given Id")
            
        fav_recipe = Favorite()
        fav_recipe.user = user
        fav_recipe.recipe = recipe
        fav_recipe.save()
        
        recipe.likes += 1
        recipe.save()

        recipe_details ={
            "id": fav_recipe.id,
            "recipe_id": recipe.id,
            "likes":recipe.likes,   
            "name": recipe.name,
        }
            
        return ApiResponse.success(data=recipe_details, message="Recipe Added to Favorites Successfully")

    
    def get_fav_recipes(self):
        request = self.request

        token = self.token_service.get_token_from_request(request)
        
        if not token:
            return ApiResponse.general_error(message="Not a valid token")
        
        user = self.token_service.get_user_from_token(token)

        if not user:
            raise GeneralException('User not found')
        
        fav_recipes = Favorite.objects.filter(user=user)

        fav_recipe_list = []
        for fav in fav_recipes:

            recipe = Recipe.objects.filter(id=fav.recipe_id).first()

            recipe_details ={
                "id":fav.id,
                "recipe_id": recipe.id,
                "likes":recipe.likes,   
                "user_id":recipe.user.id,
                "name": recipe.name,
                "description": recipe.description,
                "ingredients": [],
            }
            
            ingredients = Ingredient.objects.filter(recipe=recipe)

            for ingredient in ingredients:
                ingredient_details ={
                    "id": ingredient.id,
                    "name": ingredient.name,
                    "quantity": ingredient.quantity,
                    "recipe_id": recipe.id
                }
                recipe_details['ingredients'].append(ingredient_details)

            fav_recipe_list.append(recipe_details)

        return ApiResponse.success(data=fav_recipe_list)


    def get_favorite_recipe_details(self):
        
        request = self.request
       
        token = self.token_service.get_token_from_request(request)
        
        if not token:
            return ApiResponse.general_error(message="Not a valid token")

        user = self.token_service.get_user_from_token(token)

        if not user:
            return ApiResponse.general_error(message="User not found with this token")

        id = request.GET.get('id')

        if not id:
            return ApiResponse.general_error(message="Query Parameter 'id' missing")

        fav_recipe = Favorite.objects.filter(id=id).first()

        if not fav_recipe:
            return ApiResponse.general_error(message="Recipe not found with the given Id")

        recipe = Recipe.objects.filter(id=fav_recipe.recipe.id).first()
        
        if not recipe:
            return ApiResponse.general_error(message="Recipe not found with the given Id")
        
        favorite_recipe = {
            "id":fav_recipe.id,
        }

        favorite_recipe['recipe_details'] ={
            "id": recipe.id,
            "likes":recipe.likes,   
            "name": recipe.name,
            "user_id":recipe.user.id,
            "description": recipe.description,
            "ingredients": [],
        }
        
        ingredients = Ingredient.objects.filter(recipe=recipe)

        for ingredient in ingredients:
            ingredient_details ={
                "id": ingredient.id,
                "name": ingredient.name,
                "quantity": ingredient.quantity,
                "recipe_id": recipe.id
            }
            favorite_recipe['recipe_details']['ingredients'].append(ingredient_details)

        return ApiResponse.success(data=favorite_recipe)    

    def delete_fav_recipe(self):

        request = self.request
       
        token = self.token_service.get_token_from_request(request)
        
        if not token:
            return ApiResponse.general_error(message="Not a valid token")

        user = self.token_service.get_user_from_token(token)

        if not user:
            return ApiResponse.general_error(message="User not found with this token")

        id = request.GET.get('id')

        if not id:
            return ApiResponse.general_error(message="Query Parameter 'id' missing")

        fav_recipe = Favorite.objects.filter(id=id).first()
        
        if not fav_recipe:
            return ApiResponse.general_error(message="Recipe not found in the Favorites")

        fav_recipe.delete()

        return ApiResponse.success(message="Recipe Removed from the Favorites Successfully")
