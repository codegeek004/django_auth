from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from rest_framework.reverse import Reverse

@api_view(['GET'])
def index_view(request):
    if request.method == 'GET':
        return Response({"message" : "Welcome to OIDC authentication api"})

    
## serializers

from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.Serializer):
    role = serializers.CharField(max_length=100, default="user")
    



