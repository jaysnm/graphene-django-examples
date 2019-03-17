from django.contrib.auth.mixins import LoginRequiredMixin
from graphene_django.views import GraphQLView

class ProtectedGraphiQL(LoginRequiredMixin,GraphQLView):
    login_url = '/admin/'
        
