
import email
import jwt

from api.models import UserProfile

class TokenService:
    def __init__(self):
        pass

    _key = "51ads5f15a1sdf51a4sdf51asdf514asdf654asdf654asdf654a"
    _algorithm = "HS256"

    def create_token(self, user):
        encoded = jwt.encode({"username": user.email, "id": user.id}, self._key, algorithm=self._algorithm)
        return encoded

    def get_token(self, user):
        return self.create_token(user)

    def get_token_from_request(self, request):
        try:
            authorization = request.META.get('HTTP_AUTHORIZATION')
            if not authorization:
                return None
            bearer, token = authorization.split()
            return token
        except:
            return None

    def get_user_from_token(self, token):
        try:
            decoded = jwt.decode(token, self._key, algorithms=self._algorithm)
            user = UserProfile.objects.filter(email=decoded["username"]).first()
            if not user:
                return None
            return user
        except BaseException as e:
            print("error: get_user_from_token")
            print(e)
            return None