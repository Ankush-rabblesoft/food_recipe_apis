
import re
from django.db.models import Q

from api.exceptions.general_exception import GeneralException
from api.models import Recipe, Ingredient
from api.services.api_response import ApiResponse
from api.services.token_service import TokenService


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

class Recipes():

    request = None
    token_service = None

    def __init__(self, request):

        self.request = request
        self.token_service = TokenService()
    
    def get_recipes(self):
        request = self.request

        token = self.token_service.get_token_from_request(request)
        
        if not token:
            return ApiResponse.general_error(message="Not a valid token")
        
        user = self.token_service.get_user_from_token(token)

        if not user:
            raise GeneralException('User not found')

        recipes = Recipe.objects.filter(user=user)
        recipes_list = []

        for recipe in recipes:

            recipe_details ={
                "id": recipe.id,
                "user_id":recipe.user.id,
                "likes":recipe.likes,
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

            recipes_list.append(recipe_details)

        return ApiResponse.success(data=recipes_list)

    def add_recipe(self):
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

        name = request_data.get('name')
        description = request_data.get('description')
        ingredients = request_data.get('ingredients')
        
        if not ingredients:
            raise GeneralException('Ingredients Array Parameter is required')

        recipe = Recipe()
        recipe.name = name
        recipe.description = description
        recipe.user = user
        recipe.save()

        for item in ingredients:
            ingredient = Ingredient()
            ingredient.recipe = recipe
            ingredient.name = item['name']
            ingredient.quantity = item['quantity']
            ingredient.save()
        
        recipe_details ={
            "id": recipe.id,
            "name": recipe.name,
            "description": recipe.description,
            "ingredients": ingredients,
        }
            
        return ApiResponse.success(data=recipe_details, message="Recipe Added Successfully")

    def get_recipe_details(self):
        
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

        recipe = Recipe.objects.filter(id=id).first()
        
        if not recipe:
            return ApiResponse.general_error(message="Recipe not found with the given Id")

        recipe_details ={
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
            recipe_details['ingredients'].append(ingredient_details)

        return ApiResponse.success(data=recipe_details)


    def recipes_listing(self):
        
        recipes = Recipe.objects.all()
                
        recipes_list = []

        for recipe in recipes:

            recipe_details ={
                "id": recipe.id,
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

            recipes_list.append(recipe_details)

        return ApiResponse.success(data=recipes_list)

    def delete_recipe(self):
        
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

        recipe = Recipe.objects.filter(id=id).first()
        
        if not recipe:
            return ApiResponse.general_error(message="Recipe not found with the given Id")

        recipe.delete()

        return ApiResponse.success(message="Recipe Deleted Successfully")

    def update_recipe(self):
        
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
            return ApiResponse.general_error(message="User not found with this token")

        id = request.GET.get('id')

        if not id:
            return ApiResponse.general_error(message="Query Parameter 'id' missing")

        name = request_data.get("name", user.name)
        description = request_data.get('description')

        recipe = Recipe.objects.filter(id=id).first()

        if not recipe:
            return ApiResponse.general_error(message="Recipe not found with the given Id")

        ingredients = request_data.get('ingredients')
        
        if not ingredients:
            raise GeneralException('Ingredients Array Parameter is required')

        recipe.name = name
        recipe.description = description
        recipe.user = user
        recipe.save()
        
        for item in ingredients:
            ingredient = Ingredient.objects.filter(name=item['name'], recipe=recipe).first()

            if not ingredient:
                ingredient = Ingredient()   
                ingredient.recipe = recipe
                ingredient.name = item['name']
                ingredient.quantity = item['quantity']
                ingredient.save()
        
        recipe_details ={
            "id": recipe.id,
            "likes":recipe.likes,
            "name": recipe.name,
            "description": recipe.description,
            "ingredients": ingredients,
        }

        return ApiResponse.success(data=recipe_details, message="Recipe updated successfully")

    def search_recipe(self):
        request = self.request

        token = self.token_service.get_token_from_request(request)
        user = self.token_service.get_user_from_token(token)

        if not user:
            return ApiResponse.general_error(message="User not found with this token")

        keyword = request.GET.get('key')

        if not keyword:
            return ApiResponse.general_error(message="Query Parameter 'key' missing")

        qs = Q(name__icontains=keyword) | Q(description__icontains=keyword)
        
        recipes = Recipe.objects.filter(qs)

        print("recipes all ",recipes)
        recipes_list = []

        for recipe in recipes:

            recipe_details ={
                "id": recipe.id,
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

            recipes_list.append(recipe_details)

        response = {
            "no_of_results" : len(recipes),
            "recipes_list" : recipes_list
        }
        return ApiResponse.success(data=response)