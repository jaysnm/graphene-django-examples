from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from ingredients.views import ProtectedGraphiQL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('graphql/', csrf_exempt(ProtectedGraphiQL.as_view(graphiql=True))),
]