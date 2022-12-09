
import re
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q

from api.exceptions.general_exception import GeneralException
from api.forms.auth_forms import RegistrationForm, LoginForm,  UpdatePasswordForm
from api.models import UserProfile
from api.services.api_response import ApiResponse
from api.services.token_service import TokenService

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

class Auth():

    request = None
    token_service = None

    def __init__(self, request):

        self.request = request
        self.token_service = TokenService()

    def register(self):
        
        request = self.request
        request_data = request.json

        if not request_data:
            raise GeneralException("Request data not valid")

        if not request.method=="POST":
            raise GeneralException("Request method should be POST")
            
        name = request_data.get("name")
        email = request_data.get("email")
        password = request_data.get("password")
        address = request_data.get('address')
        city = request_data.get('city')
        state = request_data.get('state')
                  
        form = RegistrationForm(request_data)

        if not form.is_valid():

            message = "Parameter missing"
            messages = {}
            for error in form.errors:
                messages[error] = striphtml(str(form.errors[error]))

            raise GeneralException({
                    "message": message,
                    'errors': messages
                })

        user = UserProfile()
        user.name = name
        user.email = email
        user.address = address
        user.city = city
        user.state = state 
        user.password = make_password(password)
        user.save()

        data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "address": user.address,
            "city": user.city,
            "state": user.state
        }

        return ApiResponse.success(data=data, message="User registered successfully")

    def login(self):
        
        request = self.request
        request_data = request.json

        if not request_data:
            raise GeneralException("Request data not valid")

        if not request.method=="POST":
            raise GeneralException("Request method should be POST")

        email = request_data.get("email")
        password = request_data.get("password")

        form = LoginForm(request_data)

        if not form.is_valid():

            message = "Parameter missing"
            messages = {}
            for error in form.errors:
                messages[error] = striphtml(str(form.errors[error]))

            raise GeneralException({
                    "message": message,
                    'errors': messages
                })

        user = UserProfile.objects.filter(email=email).first()

        if not user:
            raise GeneralException("No User registerd with this email")

        result = check_password(password,user.password)
        
        if not result:
            raise GeneralException("Incorrect Password")

        data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "address": user.address,
            "city": user.city,
            "state": user.state,
        }
        data["token"] = self.token_service.get_token(user)

        return ApiResponse.success(data=data, message="User Logged in successfully")

    def logout(self):

        request = self.request

        token = self.token_service.get_token_from_request(request)
        
        if not token:
            return ApiResponse.general_error(message="Not a valid token")

        user = self.token_service.get_user_from_token(token)

        if not user:
            return ApiResponse.general_error(message="User not found with this token")

        return ApiResponse.success(message="User Logged out successfully")

    def update_password(self):
        
        request = self.request
        request_data = request.json

        if not request_data:
            raise GeneralException("Request data not valid")

        if not request.method=="POST":
            raise GeneralException("Request method should be POST")
            
        current_pass = request_data.get("current_pass")
        new_pass = request_data.get("new_pass")
        confirm_pass= request_data.get("confirm_pass")

        form = UpdatePasswordForm(request_data)

        if not form.is_valid():

            message = "Parameter missing"
            messages = {}
            for error in form.errors:
                messages[error] = striphtml(str(form.errors[error]))

            raise GeneralException({
                    "message": message,
                    'errors': messages
                })

        token = self.token_service.get_token_from_request(request)
        
        if not token:
            return ApiResponse.general_error(message="Not a valid token")

        user = self.token_service.get_user_from_token(token)

        if not user:
            return ApiResponse.general_error(message="User not found with this token")
        
        nuser = UserProfile.objects.filter(email=user.email).first()

        if not nuser:
            raise GeneralException("Incorrect Email")

        result = check_password(current_pass,user.password)
        
        if not result:
            raise GeneralException("Incorrect Password")

        if not new_pass == confirm_pass:
            raise GeneralException("confirm Password did not match")

        nuser.password = make_password(confirm_pass)
        nuser.save()

        return ApiResponse.success(message="Password updated successfully")
    
    def update_profile(self):
        
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

        name = request_data.get("name", user.name)
        email = request_data.get("email", user.email)
        address = request_data.get('address', user.address)
        city = request_data.get('city', user.city)
        state = request_data.get('state', user.state)
        
        user.name = name
        user.email = email
        user.address = address
        user.city = city
        user.state = state
        user.save()

        data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "address": user.address,
            "city": user.city,
            "state": user.state,
        }

        return ApiResponse.success(data=data, message="Profile updated successfully")
    
    def get_profile_by_user(self):
        
        request = self.request
       
        token = self.token_service.get_token_from_request(request)
        
        if not token:
            return ApiResponse.general_error(message="Not a valid token")

        user = self.token_service.get_user_from_token(token)

        if not user:
            return ApiResponse.general_error(message="User not found with this token")

        data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "address": user.address,
            "city": user.city,
            "state": user.state,
        }

        return ApiResponse.success(data=data)

    def dlt_user(self):
        
        request = self.request
       
        token = self.token_service.get_token_from_request(request)
        
        if not token:
            return ApiResponse.general_error(message="Not a valid token")

        user = self.token_service.get_user_from_token(token)

        if not user:
            return ApiResponse.general_error(message="User not found with this token")

        user.delete()

        return ApiResponse.success(message="User Deleted Successfully")

    def users_listing(self):
        
        users = UserProfile.objects.all()
                
        users_list = []

        for user in users:

            user_details ={
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "city": user.city,
                "state": user.state,
            }

            users_list.append(user_details)

        return ApiResponse.success(data=users_list)

    def search_user(self):
        request = self.request

        token = self.token_service.get_token_from_request(request)
        user = self.token_service.get_user_from_token(token)

        if not user:
            return ApiResponse.general_error(message="User not found with this token")

        keyword = request.GET.get('key')

        if not keyword:
            return ApiResponse.general_error(message="Query Parameter 'key' missing")

        qs = Q(name__icontains=keyword) | Q(email__icontains=keyword)
        
        users = UserProfile.objects.filter(qs)

        users_list = []

        for user in users:

            user_details ={
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "address": user.address,
                "city": user.city,
                "state": user.state,
            }

            users_list.append(user_details)

        response = {
            "no_of_results" : len(users),
            "users_list" : users_list
        }
        return ApiResponse.success(data=response)
