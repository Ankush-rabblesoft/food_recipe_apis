from django.http import JsonResponse


class ApiResponse:

    def __init__(self):
        pass

    @staticmethod
    def success(data={}, message="Success", code=200):
        response = {
            "data": data,
            "message": message,
            "code": code
        }
        return JsonResponse(response)

    @staticmethod
    def general_error(data={}, message="Success", code=422):
        response = {
            "data": data,
            "message": message,
            "code": code
        }
        return JsonResponse(response)

    @staticmethod
    def internal_error(error=None, message="Some Internal error occurred.", code=500):
        print(error)
        response = {
            "message": message,
            "code": code
        }
        return JsonResponse(response)
