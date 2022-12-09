
import traceback
from django.views.decorators.csrf import csrf_exempt

from api.decorators.decorators import auth_api
from api.controllers.classes.auth import Auth
from api.exceptions.general_exception import GeneralException
from api.services.api_response import ApiResponse


@csrf_exempt
@auth_api
def register_user(request):
    try:

        auth = Auth(request)
        return auth.register()

    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)

@csrf_exempt
@auth_api
def login_user(request):
    try:

        auth = Auth(request)
        return auth.login()

    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)

@csrf_exempt
@auth_api
def logout_user(request):
    try:

        auth = Auth(request)
        return auth.logout()

    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)

@csrf_exempt
@auth_api
def reset_password(request):
    try:

        auth = Auth(request)
        return auth.update_password()

    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)
    
@csrf_exempt
@auth_api
def edit_profile(request):
    try:

        auth = Auth(request)
        return auth.update_profile()

    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)

@csrf_exempt
@auth_api
def get_user_profile(request):
    try:

        auth = Auth(request)
        return auth.get_profile_by_user()

    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)

@csrf_exempt
@auth_api
def delete_user(request):
    try:

        auth = Auth(request)
        return auth.dlt_user()

    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)

@csrf_exempt
@auth_api
def user_listing(request):
    try:

        auth = Auth(request)
        return auth.users_listing()

    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)

@csrf_exempt
@auth_api
def search_user(request):
    try:
        auth = Auth(request)
        return auth.search_user()
    except GeneralException as e:
        return ApiResponse.general_error(message = e.message)

    except BaseException as e:
        tb = traceback.format_exc()
        print(tb)

        return ApiResponse.internal_error(e, message=e.message)
