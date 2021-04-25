import datetime 
import uuid

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import JsonResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes, api_view
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from .serializers import CreatePostSerializer, UpdatePostSerializer, RetrievePostSerializer, DeletePostSerializer, PostsLikeSerializer, PostsUnlikeSerializer
from user.models import User
from user.utils import get_object_or_401
from .models import Post

class PostCreate(APIView):

    parser_classes = [FormParser, JSONParser, MultiPartParser]

    def get_permissions(self):

        self.permission_classes = [IsAuthenticated, ]
        return super(PostCreate, self).get_permissions()


    def post(self, request, *args, **kwargs):

        serializer = CreatePostSerializer(context={'user': request.user}, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse({'response': 'Post as been registered'}, status=status.HTTP_201_CREATED)

        return JsonResponse({
            'errors': serializer.errors,
        }, status=status.HTTP_404_NOT_FOUND)
        
class PostRetriveUpdateDestroy(APIView):

    parser_classes = [FormParser, JSONParser, MultiPartParser]

    def get_queryset(self, request):
        return Post.objects.filter(public_id=self.kwargs.get('public_id'), is_active=True)
    
    def get(self, request, *args, **kwargs):
        
        instance = get_object_or_404(Post, public_id=self.kwargs.get('public_id'), is_active=True)
        get_queryset = self.get_queryset(request)
        serializer = RetrievePostSerializer(get_queryset[0], context={'user': request.user})
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
                
    def put(self, request, *args, **kwargs):
        
        instance = get_object_or_401(Post, public_id=self.kwargs.get('public_id'), user=self.request.user, is_active=True)
        get_queryset = self.get_queryset(request)
        serializer = UpdatePostSerializer(get_queryset, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'response': 'Post as been updated'}, status=status.HTTP_200_OK)

        return JsonResponse({
            'errors': serializer.errors,
        }, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, *args, **kwargs):
        
        instance = get_object_or_401(Post, public_id=self.kwargs.get('public_id'), user=self.request.user, is_active=True)
        instance.is_active = False
        instance.save()
        
        return JsonResponse({'response': 'Post as been deleted'}, status=status.HTTP_200_OK)

class PostList(APIView):

    parser_classes = [FormParser, JSONParser, MultiPartParser]

    def get_queryset(self, request):
        return Post.objects.filter(is_active=True)
    
    def get(self, request, *args, **kwargs):
        get_queryset = self.get_queryset(request)
        serializer = RetrievePostSerializer(get_queryset, context={'user': request.user}, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    

class PostsLike(APIView):

    parser_classes = [FormParser, JSONParser, MultiPartParser]

    def get_permissions(self):
        
        self.permission_classes = [IsAuthenticated, ]
        return super(PostsLike, self).get_permissions()

    def get_queryset(self, request):
        return Post.objects.filter(public_id=self.kwargs.get('public_id'), is_active=True)
    
    def post(self, request, *args, **kwargs):
        
        instance = get_object_or_404(Post, public_id=self.kwargs.get('public_id'), is_active=True)
        get_queryset = self.get_queryset(request)
        serializer = PostsLikeSerializer(get_queryset[0], context={'user': request.user}, data=request.data)
        
        if serializer.is_valid():
            like = serializer.create(serializer.validated_data)
            like.save()
            return JsonResponse({"response": "Like registered"}, safe=False, status=status.HTTP_200_OK)
        
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_404_NOT_FOUND)
        

class PostsUnlike(APIView):

    parser_classes = [FormParser, JSONParser, MultiPartParser]

    def get_permissions(self):
        
        self.permission_classes = [IsAuthenticated, ]
        return super(PostsUnlike, self).get_permissions()

    def get_queryset(self, request):
        return Post.objects.filter(public_id=self.kwargs.get('public_id'), is_active=True)
    
    def post(self, request, *args, **kwargs):
        
        instance = get_object_or_404(Post, public_id=self.kwargs.get('public_id'), is_active=True)
        get_queryset = self.get_queryset(request)
        serializer = PostsUnlikeSerializer(get_queryset[0], context={'user': request.user}, data=request.data)
        
        if serializer.is_valid():
            unlike = serializer.create(serializer.validated_data)
            unlike.save()
            return JsonResponse({"response": "Unlike registered"}, safe=False, status=status.HTTP_200_OK)
        
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_404_NOT_FOUND)
        