from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='ingredients',on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
