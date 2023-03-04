from django.db import models

# Create your models here.

class SecuredAccess(models.Model):

    key = models.TextField(max_length=50)
    value = models.TextField(max_length=300)    
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)    

class HostList(models.Model):
    host_ip = models.TextField(default="", max_length=14)
    is_blacklisted = models.BooleanField(False)
    reson_for_blacklist = models.CharField(default="",null=True, blank=True)
    stored_by = models.TextField(max_length=115)
