import uuid

from django.db import models
from django.contrib import admin
from django.core.validators import MaxValueValidator
from django.contrib.postgres.fields import ArrayField

from user.models import User


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, blank=False)
    title = models.CharField(max_length=200, blank=False, null=False)
    image_url = models.CharField(max_length=200, blank=False, null=False)
    content = models.CharField(max_length=10000, blank=False, null=False)
    
    # State
    views = models.IntegerField(validators=[MaxValueValidator(10)], default=0, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    
    # User
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.UUIDField(default=uuid.uuid4, editable=False)
    
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class UnLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    public_id = models.UUIDField(default=uuid.uuid4, editable=False)
    
    created_at = models.DateTimeField(auto_now_add=True, blank=False, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)
    
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)    

class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "public_id",
        "title",
        "image_url",
        "content",
        "views",
        "created_at",
        "updated_at",
        "is_active",
        "user"
    )

admin.site.register(Post, PostAdmin)