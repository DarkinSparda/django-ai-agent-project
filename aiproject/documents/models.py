from django.conf import settings
from django.db import models
from django.utils import timezone
# Create your models here.

User = settings.AUTH_USER_MODEL


class Document(models.Model):
    owner = models.ForeignKey(User, on_delete= models.CASCADE) 
    title = models.CharField(default="Title", max_length=200)
    content = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    active_at = models.DateTimeField(auto_now_add=False, auto_now=False, default=timezone.now())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

