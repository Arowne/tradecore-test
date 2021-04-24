import datetime 
import uuid

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes, api_view
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from .serializers import CreatePostSerializer, UpdatePostSerializer, RetrievePostSerializer, DeletePostSerializer, PostsLikeSerializer, PostsUnlikeSerializer
from user.models import User
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

            return JsonResponse({'response': 'Post as been registered'}, status=201)

        return JsonResponse({
            'errors': serializer.errors,
        }, status=404)
        
class PostRetriveUpdateDestroy(APIView):

    parser_classes = [FormParser, JSONParser, MultiPartParser]

    def get_permissions(self):
        
        is_admin = ["DELETE", "PUT"]
        
        if self.request.method in is_admin:
            self.permission_classes = [IsAdminUser, ]

        return super(PostRetriveUpdateDestroy, self).get_permissions()

    def get_queryset(self, request):
        
        return Post.objects.filter(public_id=self.kwargs.get('public_id'), is_active=True)
    
    def get(self, request, *args, **kwargs):
        
        instance = get_object_or_404(Post, public_id=self.kwargs.get('public_id'), is_active=True)
        get_queryset = self.get_queryset(request)
        serializer = RetrievePostSerializer(get_queryset[0])
        return JsonResponse(serializer.data, safe=False, status=200)
                
    def put(self, request, *args, **kwargs):
        
        instance = get_object_or_404(Post, public_id=self.kwargs.get('public_id'), is_active=True)
        get_queryset = self.get_queryset(request)
        serializer = UpdatePostSerializer(get_queryset, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'response': 'Post as been updated'}, status=200)

        return JsonResponse({
            'errors': serializer.errors,
        }, status=404)
    
    def delete(self, request, *args, **kwargs):
        
        instance = get_object_or_404(Post, public_id=self.kwargs.get('public_id'), is_active=True)
        instance.is_active = False
        instance.save()
        
        return JsonResponse({'response': 'Post as been deleted'}, status=200)

class PostList(APIView):

    parser_classes = [FormParser, JSONParser, MultiPartParser]


    def get_queryset(self, request):
        return Post.objects.filter(is_active=True)
    
    def get(self, request, *args, **kwargs):
        get_queryset = self.get_queryset(request)
        serializer = RetrievePostSerializer(get_queryset, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
    

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
            return JsonResponse(serializer.data, safe=False, status=200)
        
        return JsonResponse(serializer.errors, safe=False, status=404)
        

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
            return JsonResponse(serializer.data, safe=False, status=200)
        
        return JsonResponse(serializer.errors, safe=False, status=404)
        