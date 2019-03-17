import graphene 
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
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

class CreateCategoryType(graphene.InputObjectType):
    """
    Relay method to create category
    """
    name = graphene.String(required=True)

class CreateCategory(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.Argument(CreateCategoryType)
    new_category=graphene.Field(CategoryNode)
    @classmethod
    def mutate_and_get_payload(cls, info, name):
        if info.context.user.is_anonymous:
            return cls(new_category=None,errors="You must login first")
        else:
            category = Category.objects.create(user=info.context.user,name=name)
            return cls(new_category=category)

class UpdateCategory(graphene.relay.ClientIDMutation):
    class Input:
        category = graphene.Argument(CreateCategoryType)
        id = graphene.String(required=True)
    errors = graphene.List(graphene.String)
    updated_category = graphene.Field(CategoryNode)
    @classmethod
    def mutate_and_get_payload(cls, args, context, info):
        try:
            category = Category.objects.get(pk=args.get('id'))
            if category:
                category.name = args.get('name')
                category.save()
                return cls(updated_category=category)
        except ValueError as err:
            """ fields = err.message_dict.keys()
            messages = ['; '.join(m) for m in err.message_dict.values()]
            errors = [i for pair in zip(fields, messages) for i in pair] """
            return cls(updated_category=None, errors=err)
        

class Query(graphene.ObjectType):
    category = graphene.relay.Node.Field(CategoryNode)
    categories = DjangoFilterConnectionField(CategoryNode,description="All ingredients or a filter set")
    ingredient = graphene.relay.Node.Field(IngredientNode)
    ingredients = DjangoFilterConnectionField(IngredientNode,description="All ingredients or a filter set")
    def resolve_categories(self, info, **kwargs):
        try:
            if info.context.user.is_anonymous:
                return Category.objects.none()
            else:
                return Category.objects.all()
        except (Exception) as error:
            return error

class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field(description="Relay method to create category")
    update_category = UpdateCategory.Field(description="Relay method to update category")
    