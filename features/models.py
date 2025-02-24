from django.db import models
from django.contrib.auth.models import User


class DeletedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)


class BaseModel(models.Model):
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = DeletedManager()
    
    class Meta:
        abstract = True
        

class LostItem(BaseModel):
    lost_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name="lost_by_user")
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date_lost = models.DateField()
    is_found = models.BooleanField(default=False)
    image = models.ImageField(upload_to="lost_items/", null=True, blank=True)  

class FoundItem(BaseModel):
    found_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,related_name="found_by_user")
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date_found = models.DateField()
    claimed = models.BooleanField(default=False)
    image = models.ImageField(upload_to="found_items/", null=True, blank=True) 