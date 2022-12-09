from django.db import models

from django.utils import timezone


class UserProfile(models.Model):
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    password = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(UserProfile, default=None, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class Ingredient(models.Model):
    name = models.CharField(max_length=255, null=False)
    quantity = models.CharField(max_length=255, null=False)
    recipe = models.ForeignKey(Recipe, default=None, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class Favorite(models.Model):
    recipe = models.ForeignKey(Recipe, default=None, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, default=None, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
