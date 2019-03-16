import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.contrib.auth import get_user_model
from .models import Category, Ingredient

class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        exclude_fields=('name')
        filter_fields = ['id']
        interfaces = (graphene.relay.Node,)
        
class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        only_fields =('name',"notes")
        filter_fields = {'name':['exact','icontains','istartswith'],'notes':['icontains','istartswith']}
        interfaces = (graphene.relay.Node,)


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    def mutate(self, info, username, email, password):
        user = get_user_model()(username = username, email = email)
        user.set_password(password)
        user.save()
        return CreateUser(user=user)


class Query(graphene.ObjectType):
    category = graphene.relay.Node.Field(CategoryNode)
    categories = DjangoFilterConnectionField(CategoryNode)
    ingredient = graphene.relay.Node.Field(IngredientNode)
    ingredients = DjangoFilterConnectionField(IngredientNode)
    def resolve_categories(self, info, **kwargs):
        if not info.context.user.is_authenticated:
            return Category.objects.none()
        else:
            return Category.objects.all()

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    