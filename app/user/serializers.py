import os
import asyncio
import time

from threading import Thread
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.core.validators import RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError

from .utils import ip_localisation
from .models import Login
from user.models import User


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers 

class IPOnObtainTokenPairSerializer(TokenObtainPairSerializer):

    def validate(self, data):
        
        user = authenticate(username=data["username"], password=data["password"])
        ip = self.context["request"].META.get('REMOTE_ADDR')
        
        if user:
            task = Thread(target=ip_localisation(ip, user))
            task.start()
            
        return super().validate(data)
        
        
# Create the form class.
#_UserSubscriptionSerializer
class UserSubscriptionSerializer(serializers.Serializer):

    first_name = serializers.CharField(max_length=30, validators=[RegexValidator(r'^[a-zA-ZàâäôéèëêïîçùûüÿæœÀÂÄÔÉÈËÊÏÎŸÇÙÛÜÆŒàèéìíîòóùúÀÈÉÌÍÎÒÓÙÚáéíñóúüÁÉÍÑÓÚÜ\'\- ]+$', "Please enter a valid first name. It can only contain the following special characters: -\' and space")], error_messages={
        'required': "Please enter your first name",
        'max_length': "Your first name cannot exceed 30 characters"
    })

    last_name = serializers.CharField(max_length=30, validators=[RegexValidator(r'^[a-zA-ZàâäôéèëêïîçùûüÿæœÀÂÄÔÉÈËÊÏÎŸÇÙÛÜÆŒàèéìíîòóùúÀÈÉÌÍÎÒÓÙÚáéíñóúüÁÉÍÑÓÚÜ\'\- ]+$', "Please enter a valid name. It can only contain the following special characters: -\' and a space.")],error_messages={
        'required': "Please enter your name",
        'max_length': "Your name cannot exceed 30 characters"
    })

    email = serializers.EmailField(max_length=200, error_messages={
        'required': "Please enter your email",
        'invalid' : "Please enter a valid email address in the format: exemple@exemple.com",
        'max_length': "Your email cannot exceed 200 characters"
    })
        
    password = serializers.CharField(max_length=200, validators=[RegexValidator(r'^(?=.*\d).{8,}$', "Your password must contain at least eight characters, one number and one letter.")], error_messages={
        'required': "Please enter your password",
        'max_length': "Your password cannot exceed 200 characters."
    })

    confirm_password = serializers.CharField(error_messages={
        'required': "Please confirm your password"
    })

    def __init__(self, *args, **kwargs):
        serializers.Serializer.__init__(self, *args, **kwargs)

    def validate_email(self, value):
        
        user = User.objects.filter(email=value, is_active=True).first()

        if user:
            raise ValidationError("An account already uses this email address")

        return value


    def validate_confirm_password(self, value):

        # Check if password is matching with his confirmation
        password = self.initial_data['password']

        if value != password:
            raise ValidationError("Your password confirmation must be the same as your password")
        
        return value

#_UpdateUserSerializer
class UpdateUserSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        serializers.Serializer.__init__(self, *args, **kwargs)
        self.user_id = self.context['user_id']

    first_name = serializers.CharField(max_length=200, validators=[RegexValidator(r'^[a-zA-Z\'\- ]+$', "Please enter a valid first name. It can only contain the following characters: -\and a space.")], error_messages={
        'required': "Please enter your first name",
        'max_length': "Your first name cannot exceed 200 characters"
    })

    last_name = serializers.CharField(max_length=200, validators=[RegexValidator(r'^[a-zA-Z\'\- ]+$', "Please enter a valid first name. It can only contain the following characters: -\and a space.")],error_messages={
        'required': "Please enter your name",
        'max_length': "Your name cannot exceed 200 characters"
    })

    pseudo = serializers.CharField(max_length=20,error_messages={
        'required': "Please enter your pseudo",
        'max_length': "Your name cannot exceed 20 characters"
    })

    email = serializers.EmailField(max_length=200, error_messages={
        'required': "Please enter your email",
        'invalid' : "Please enter a valid email address in the format: exemple@exemple.com",
        'max_length': "Your email cannot exceed 200 characters"
    })

    password = serializers.CharField(max_length=200, error_messages={
        'max_length': "Your password cannot exceed 200 characters."
    })

    def validate_email(self, value):

        user = User.objects.filter(email=value, is_active=True).first()
        current_user = User.objects.get(public_id = self.user_id, is_active = True)

        if user and current_user.id != user.id:
            raise ValidationError("An account already uses this email address")

        return value


    def validate_password(self, value):

        user = User.objects.get(public_id = self.user_id, is_active = True)
        password_match = check_password(value, user.password)

        if not password_match:
            raise ValidationError("Your account password was not recognized")

        return value

#_DeleteUserSerializer
class DeleteUserSerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        serializers.Serializer.__init__(self, *args, **kwargs)
        self.user_id = self.context['user_id']

    password = serializers.CharField(max_length=200, error_messages={
        'required': "Please enter your password",
        'max_length': "Your password cannot exceed 200 characters."
    })

    def validate_password(self, value):

        user = User.objects.get(public_id=self.user_id, is_active=True)

        password = self.initial_data['password']
        password_match = check_password(password, user.password)

        if not password_match:
            raise ValidationError("Your account password was not recognized")


        return value

class ListLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = Login
        fields = ['location', 'is_holiday']


class ListUserSerializer(serializers.ModelSerializer):
    
    login_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "login_list"]
    
    def get_login_list(self, obj):
        return ListLoginSerializer(obj.login_set.all(), many=True).data