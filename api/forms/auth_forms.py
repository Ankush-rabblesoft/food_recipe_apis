
from django import forms
from django.core.exceptions import ValidationError

from api.models import UserProfile


class RegistrationForm(forms.Form):

    def email_valid(value):
        
        user_email = UserProfile.objects.filter(email = value).first()
        
        if user_email :
            raise ValidationError("Email already registered")

    name = forms.CharField(max_length= 255)
    email = forms.EmailField(validators= [email_valid])
    password = forms.CharField(max_length= 255)

    class Meta:

        name = {
            "required": True,
        }
        email = {
            "required": True,
        }
        password = {
            "required": True,
        }
        
class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField()

    class Meta:

        email = {
            "required": True,
        }
        password = {
            "required": True,
        }

class UpdatePasswordForm(forms.Form):
    
    current_pass = forms.CharField()
    new_pass = forms.CharField()
    confirm_pass = forms.CharField()

    class Meta:

        current_pass = {
            "required": True,
        }
        new_pass = {
            "required": True,
        }
        confirm_pass = {
            "required": True,
        }
