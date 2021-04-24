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
        fields = ['email']

class ListLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['created_at']

class ListUnlikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnLike
        fields = ['created_at']

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
    like =  serializers.SerializerMethodField(read_only=True)
    unlike = serializers.SerializerMethodField(read_only=True)

    def get_like(self, obj):
        return ListLikeSerializer(obj.like_set.filter(is_active=True), many=True).data

    def get_unlike(self, obj):
        return ListUnlikeSerializer(obj.unlike_set.filter(is_active=True), many=True).data

    class Meta:
        model = Post
        fields = ["public_id", "title", "image_url", "content", "user", "like", "unlike"]

    
class RetrieveAllPostSerializer(serializers.ModelSerializer):

    user = ListUserSerializer(many=False)

    class Meta:
        model = Post
        fields = ["public_id", "title", "image_url", "content", "user"]


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
            unlike.save()

        if unlike:
            unlike.is_active = False
        else:
            unlike = UnLike.objects.create(post=self.instance, user=self.context['user'])
            
        return unlike