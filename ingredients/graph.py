import graphene
from graphene_django.types import DjangoObjectType
from .models import Category, Ingredient

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

class Query(object):
    categories = graphene.List(CategoryType)
    ingredients = graphene.List(IngredientType)
    category = graphene.Field(CategoryType, id=graphene.Int(), name=graphene.String())
    Ingredient = graphene.Field(IngredientType,id=graphene.Int(),name=graphene.String())
    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()
    def resolve_ingredients(self, info, **kwargs):
        return Ingredient.objects.all()
    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')
        if id is not None:
            return Category.objects.get(pk=id)
        elif name is not None:
            return Category.objects.get(name=name)
        return None
    def resolve_ingredient(self, info, **kwargs):
        id = kwargs.get("id")
        name = kwargs.get("name")
        if id is not None:
            return Ingredient.objects.get(pk=id)
        elif name is not None:
            return Ingredient.objects.get(name=name)
        return None