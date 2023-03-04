from django.shortcuts import render
from .models import SecuredAccess, HostList

# Create your views here.

def get_value(key,ip):

    resources = SecuredAccess.objects.all()
    print(resources.__dict__)
    hosts = HostList.objects.all()
    print(hosts.__dict__)
    