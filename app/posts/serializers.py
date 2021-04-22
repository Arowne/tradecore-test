import os

from rest_framework import generics
from rest_framework import serializers 
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.core.validators import RegexValidator, FileExtensionValidator

from .models import Post
from user.models import User
# Create the form class.

class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email']

class CreatePostSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
      user = self.context['user']
      validated_data["is_active"] = True 
      post = Post.objects.create(user=user, **validated_data)
      return post
  
    class Meta:
        model = Post
        fields = ["title", "image_url", "content"]
        
class UpdatePostSerializer(serializers.ModelSerializer):
    
    def update(self, instance, validated_data):
      validated_data["is_active"] = True 
      post = instance.update(**validated_data)
      return post
  
    class Meta:
        model = Post
        fields = ["title", "image_url", "content"]

class DeletePostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = []
          
class RetrievePostSerializer(serializers.ModelSerializer):
    
    user = ListUserSerializer(many=False)
    
    class Meta:
        model = Post
        fields = ["public_id", "title", "image_url", "content", "user"]