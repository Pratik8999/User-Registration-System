from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.db.utils import IntegrityError
from django.core.mail import send_mail
from datetime import datetime
import random

HOST = "http://localhost:8000/"

@csrf_exempt
def verify_user(request,emailid):
    user = get_object_or_404(CustomUser,email=emailid)
    user.is_verified=True
    user.save()
    return JsonResponse({"Response":"Email Confirmed"}, status=status.HTTP_200_OK)
    

def send_email(name, email, link):
     send_mail(
          subject="Confirm Email for Registration Site",
          message=f"Hii {name},\n\nWelcome to User Registration System.\nPlease click on below link to confirm your Email.\nLink: {link}\n\nRegards,\nTeam Registration.",
          from_email="priks9998@gmail.com",
          recipient_list=[email],
          fail_silently=False
     )     

@csrf_exempt
def register_user(request):
    # Data Sanitization.
        if not request.method == "POST":
            return JsonResponse({'Error': 'Please Send a POST request with Valid Parameters Only.'},status=status.HTTP_400_BAD_REQUEST)
        data = JSONParser().parse(request)
        user_data = CustomUserSerializer(data=data)       

        if user_data.is_valid():
            try:
                user_data.validated_data["calculated_BMI"] = user_data.caculate_BMI(user_data.validated_data["weight_kg"],user_data.validated_data["height_cm"])    
                user_data.save()   
                send_email(user_data.validated_data['full_name'], user_data.validated_data['email'] , link=HOST+f"/user/confirm/{user_data.validated_data['email']}/")
            except IntegrityError:
                return JsonResponse({'Error':'Provided Email Already Registered.Please try another email Id.'},status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                 return JsonResponse(user_data.data, status=status.HTTP_201_CREATED)
            
        return JsonResponse(user_data.errors, status=status.HTTP_400_BAD_REQUEST)


def generate_session_token(length=20):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(65, 90)] + [str(i) for i in range(10)]) for _ in range(length))


@csrf_exempt
def login(request):
    
    if not request.method=="POST":
         return JsonResponse({'Error': 'Please Send a POST request with Valid Parameters Only.'},status=status.HTTP_400_BAD_REQUEST)
    email =  request.POST['email']
    password = request.POST['password']   
    
    current_user = get_object_or_404(CustomUser,email=email,password=password)
    if current_user.is_active or not current_user.is_verified:
        return JsonResponse({'response':"User Session Already Exists. Or Make Sure You've confirmed your email."}, status=status.HTTP_401_UNAUTHORIZED)                  
    else:
        current_user.session_token = generate_session_token()
        current_user.is_active = True
        current_user.last_login = datetime.now()
        current_user.save()
        return JsonResponse(CustomUserSerializer(current_user).data, status=status.HTTP_200_OK)       
 

@csrf_exempt
def logout(request):    
    if not request.method=="POST":
         return JsonResponse({'Error': 'Please Send a POST request with Valid Parameters Only.'},status=status.HTTP_400_BAD_REQUEST)
    
    email = request.POST["email"]
    current_user = get_object_or_404(CustomUser,email=email)
    if not current_user.is_active:
        return JsonResponse({'Response':'Invalid Request. User Already logged out.'},status=status.HTTP_400_BAD_REQUEST)
    else:
        current_user.session_token = None
        current_user.is_active = False
        current_user.save()
        return JsonResponse({'response':'Success'}, status=status.HTTP_200_OK)
    

@csrf_exempt
def user_details(request, email):
    """
    Retrieve, update or delete a user data.
    """
    user = get_object_or_404(CustomUser,email=email)
    if not user.is_active or not user.is_verified:
        return JsonResponse({'response':"Invalid User Session. Please login first Or Make Sure You've confirmed your email."}, status=status.HTTP_401_UNAUTHORIZED)            
    
    if request.method == 'GET':    
        serializer = CustomUserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        user.modified_date = datetime.now()
        serializer = CustomUserSerializer(user, data=data)
        if serializer.is_valid():
            try:
                 serializer.save()
            except IntegrityError as ie:
                 return JsonResponse({'Error':'Provided Email Already Registered.Please try another email Id.'},status=status.HTTP_406_NOT_ACCEPTABLE)
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    
    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'Response':'Successfully Deleted Requested Resource.'}, status=status.HTTP_200_OK)

def reset_password(request):
    if not request.method=="POST":
         return JsonResponse({'Error': 'Please Send a POST request with Valid Parameters Only.'},status=status.HTTP_400_BAD_REQUEST)
    email = request.POST["email"]
    password = request.POST["password"]

    current_user = get_object_or_404(CustomUser,email=email)
    current_user.password = password
    current_user.save()
    return HttpResponse(status=status.HTTP_200_OK)
