import datetime 
import uuid

from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes, api_view
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import ListUserSerializer, UserSubscriptionSerializer, UpdateUserSerializer, DeleteUserSerializer, IPOnObtainTokenPairSerializer
from .models import User


class IPOnObtainTokenPair(TokenObtainPairView):
    
    def __init__(self):
        TokenObtainPairView.__init__(self)
        
    serializer_class = IPOnObtainTokenPairSerializer
    
class UserCreateRetriveUpdateDestroy(APIView):

    parser_classes = [FormParser, JSONParser, MultiPartParser]

    def get_permissions(self):

        if self.request.method != 'POST':
            self.permission_classes = [IsAuthenticated, ]

        return super(UserCreateRetriveUpdateDestroy, self).get_permissions()


    def post(self, request, *args, **kwargs):

        serializer = UserSubscriptionSerializer(data=request.data)

        if serializer.is_valid():

            data = serializer.validated_data
            user = User.objects.create_user(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                email=data.get("email"),
                username=data.get("email"),
                password=data.get("password"),
            )

            user.save()

            return JsonResponse({'response': 'User as been registered'}, status=201)

        return JsonResponse({
            'errors': serializer.errors,
        }, status=404)

    def get(self, request, *args, **kwargs):

        user_id = request.user.public_id
        user = User.objects.filter(public_id=user_id).values()
        
        return JsonResponse(list(user), safe=False, status=200)
    
    def put(self, request, *args, **kwargs):
        
        user_id = request.user.public_id
        serializer = UpdateUserSerializer(context={'user_id': user_id}, data=request.data)

        if serializer.is_valid():

            user = User.objects.get(public_id=user_id)
            data = serializer.validated_data
            
            user.first_name= data.get('first_name')
            user.last_name= data.get('last_name')
            user.email = data.get("email")
            user.username = data.get("email")
            user.pseudo = data.get("pseudo")
            user.updated_at = datetime.datetime.now()
            user.save()

            return JsonResponse({'response': 'User updated'}, status=200)

        return JsonResponse({
            'errors': serializer.errors
        }, status=404)

    def delete(self, request, *args, **kwargs):

        user_id = request.user.public_id
        serializer = DeleteUserSerializer(context={'user_id': user_id}, data=request.data)

        if serializer.is_valid():

            user = User.objects.get(public_id=user_id , is_active=True)
            user.is_active = False
            user.username = uuid.uuid4()
            user.save()

            return JsonResponse({'response': 'Account deleted'})

        return JsonResponse({
            'errors': serializer.errors
        }, status=400)

class UserList(APIView):

    parser_classes = [FormParser, JSONParser, MultiPartParser]

    def get_permissions(self):

        self.permission_classes = [IsAdminUser]
        return super(UserList, self).get_permissions()

    def get_queryset(self, request):
        return User.objects.filter(is_active=True)
    
    def get(self, request, *args, **kwargs):
        get_queryset = self.get_queryset(request)
        serializer = ListUserSerializer(get_queryset, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)