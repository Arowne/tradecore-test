import os

from rest_framework import generics
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.core.validators import RegexValidator, FileExtensionValidator

from .models import Post, UnLike, Like
from user.models import User
# Create the form class.


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class CreatePostSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = self.context['user']
        validated_data["is_active"] = True
        post = Post.objects.create(user=user, **validated_data)
        return post

    image = serializers.ImageField()
    
    class Meta:
        model = Post
        fields = ["title", "image", "content"]


class UpdatePostSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        validated_data["is_active"] = True
        post = instance.update(**validated_data)
        return post
    
    image = serializers.ImageField()
    
    class Meta:
        model = Post
        fields = ["title", "image", "content"]


class DeletePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = []


class RetrievePostSerializer(serializers.ModelSerializer):

    user = ListUserSerializer(many=False)
    like =  serializers.SerializerMethodField(read_only=True)
    unlike = serializers.SerializerMethodField(read_only=True)
    user_unlike = serializers.SerializerMethodField(read_only=True)
    user_like = serializers.SerializerMethodField(read_only=True)

    def get_like(self, obj):
        return obj.like_set.filter(is_active=True).count()

    def get_unlike(self, obj):
        return obj.unlike_set.filter(is_active=True).count()
    
    def get_user_like(self, obj):
        
        if self.context['user'].is_anonymous:
            return False
        
        return len(obj.like_set.filter(user=self.context['user'], is_active=True)) == 1

    def get_user_unlike(self, obj):
        
        if self.context['user'].is_anonymous:
            return False
        
        return len(obj.unlike_set.filter(user=self.context['user'], is_active=True)) == 1

    class Meta:
        model = Post
        fields = ["public_id", "title", "image", "content", "user", "like", "unlike", "user_like", "user_unlike"]

    
class RetrieveAllPostSerializer(serializers.ModelSerializer):

    user = ListUserSerializer(many=False)

    class Meta:
        model = Post
        fields = ["public_id", "title", "image", "content", "user"]


class PostsLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["public_id"]

    def create(self, validated_data):
        
        unlike = UnLike.objects.filter(post=self.instance, user=self.context['user'], is_active=True).first()
        like = Like.objects.filter(post=self.instance, user=self.context['user'], is_active=True).first()
        
        if unlike:
            unlike.is_active = False
            unlike.save()

        if like:
            like.is_active = False
        else:
            like = Like.objects.create(post=self.instance, user=self.context['user'])
            
        return like


class PostsUnlikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ["public_id"]
        
    def create(self, validated_data):
        unlike = UnLike.objects.filter(post=self.instance, user=self.context['user'], is_active=True).first()
        like = Like.objects.filter(post=self.instance, user=self.context['user'], is_active=True).first()
        
        if like:
            like.is_active = False
            like.save()

        if unlike:
            unlike.is_active = False
        else:
            unlike = UnLike.objects.create(post=self.instance, user=self.context['user'])
            
        return unlike