from django.contrib import admin

from api.models import *

admin.site.register(UserProfile)
admin.site.register(Recipe)
admin.site.register(Ingredient)