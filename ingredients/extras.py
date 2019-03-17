import graphene
from graphene_django.types import DjangoObjectType as DefaultObjectType
from graphene_django_extras import DjangoListObjectType, DjangoObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination
from graphene_django_extras import DjangoInputObjectType
from graphene_django_extras import DjangoObjectField, DjangoListObjectField, DjangoFilterPaginateListField, DjangoFilterListField, LimitOffsetGraphqlPagination
from .models import Ingredient

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        description = "Single ingredient type description "
        filter_fields = {
            'id': ['exact', ],
            'name': ['icontains', 'iexact'],
            'notes': ['icontains']
        }


class IngredientListType(DjangoListObjectType):
    class Meta:
        description = "Ingredients definition type"
        model = Ingredient
        pagination = LimitOffsetGraphqlPagination(default_limit=5, ordering="-name")  # ordering can be: string, tuple or list
  
class Query(graphene.ObjectType):
    extras_ingredients = DjangoListObjectField(IngredientListType, description='All Ingredients query')
    ingredient_one = DjangoFilterPaginateListField(IngredientType, pagination=LimitOffsetGraphqlPagination())
    ingredient_two = DjangoFilterListField(IngredientType)
    extras_ingredient = DjangoObjectField(IngredientType, description='Single Ingredient query')
