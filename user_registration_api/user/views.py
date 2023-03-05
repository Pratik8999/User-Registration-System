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


# Generic Email Sharing Function.
def send_email(name,email,subject="", message="", link="", default_msg=False):
     if default_msg:
         message=f"Hii {name},\n\nWelcome to User Registration System.\nPlease click on below link to confirm your Email.\nLink: {link}\n\nRegards,\nTeam Registration."
     send_mail(
          subject=subject,
          message=message,
          from_email="someone@mail.com",
          recipient_list=[email],
          fail_silently=False
     ) 


# Verify the newly registered user.
@csrf_exempt
def verify_user(request,emailid):
    user = get_object_or_404(CustomUser,email=emailid)
    user.is_verified=True
    user.modified_date = datetime.now()    
    user.save() 

    # Sending a BMI Analysis Report After Email Id Verification of User.

    message = f"""!! Congratulations {user.full_name}. You've successfully confirmed Your Email Address !!\n\nBMI Report\n-----------.
    As per the analysis of your provided data Of Your Weight:{user.weight_kg} Kg and Height:{user.height_cm} cm
    Your Body Mass Index (BMI) is {user.calculated_BMI}\n BMI Calculation Date:{user.modified_date}
    Final Conclusion on your BMI is:{user.BMI_Analyser(user.calculated_BMI)}\n\nRegards,\nTeam Registration.
    """
    send_email(name=user.full_name,email=user.email,subject="The First BMI Report",message=message)
    return JsonResponse({"Response":"Email Confirmed"}, status=status.HTTP_200_OK)
        

# Registered a New User.  
@csrf_exempt
def register_user(request):
    
    # Data Sanitization.
        if not request.method == "POST":
            return JsonResponse({'Error': 'Please Send a POST request with Valid Parameters Only.'},status=status.HTTP_400_BAD_REQUEST)
        data = JSONParser().parse(request)
        user_data = CustomUserSerializer(data=data)       

        # Creating a User with valid data and sending "Email Confirmation request".
        if user_data.is_valid():
            try:
                user_data.validated_data["calculated_BMI"] = user_data.caculate_BMI(user_data.validated_data["weight_kg"],user_data.validated_data["height_cm"])    
                user_data.save()
                send_email(user_data.validated_data['full_name'], user_data.validated_data['email'] ,subject="Confirm Email for Registration Site", link=HOST+f"/user/confirm/{user_data.validated_data['email']}/",default_msg=True)
            
            except IntegrityError:                
                # Allowing only Unique Email Ids via giving a "Meaningful API Response"
                return JsonResponse({'Error':'Provided Email Already Registered. Please try another email Id.'},status=status.HTTP_406_NOT_ACCEPTABLE)
            
            else:
                 # Final User Creation Meaningful Response.
                 return JsonResponse(user_data.data, status=status.HTTP_201_CREATED)
            
        return JsonResponse(user_data.errors, status=status.HTTP_400_BAD_REQUEST)


# User Session Token Generator.
def generate_session_token(length=20):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(65, 90)] + [str(i) for i in range(10)]) for _ in range(length))


# User Login Endpoint.
@csrf_exempt
def login(request):
    
    if not request.method=="POST":
         return JsonResponse({'Error': 'Please Send a POST request with Valid Parameters Only.'},status=status.HTTP_400_BAD_REQUEST)
    email =  request.POST['email']
    password = request.POST['password']   
    
    current_user = get_object_or_404(CustomUser,email=email,password=password)

    # Only Allowing login to Email Verified and Sessionly Inactive users. if not still a 'Meaningful API Response will be Returened'
    if current_user.is_active or not current_user.is_verified:
        return JsonResponse({'response':"User Session Already Exists. Or Make Sure You've confirmed your email."}, status=status.HTTP_401_UNAUTHORIZED)                  
    else:
        current_user.session_token = generate_session_token()
        current_user.is_active = True
        current_user.last_login = datetime.now()
        current_user.save()
        return JsonResponse(CustomUserSerializer(current_user).data, status=status.HTTP_200_OK)       
 
# Logout Endpoint.
@csrf_exempt
def logout(request):    
    if not request.method=="POST":
         return JsonResponse({'Error': 'Please Send a POST request with Valid Parameters Only.'},status=status.HTTP_400_BAD_REQUEST)
    
    email = request.POST["email"]
    current_user = get_object_or_404(CustomUser,email=email)

    # Blocking Invalid Requests by checking the current user's active status.
    if not current_user.is_active:
        return JsonResponse({'Response':'Invalid Request. User Already logged out.'},status=status.HTTP_400_BAD_REQUEST)
    else:
        current_user.session_token = None
        current_user.is_active = False
        current_user.save()
        return JsonResponse({'response':'Success'}, status=status.HTTP_200_OK)
    

# User Data - CRUD Operation Endpoint  →  ** After Login & for validated User Only **
@csrf_exempt
def user_details(request, email):
    """
    Retrieve, update or delete a user data.
    """
    user = get_object_or_404(CustomUser,email=email)
    if not user.is_active or not user.is_verified:
        return JsonResponse({'response':"Invalid User Session. Please login first Or Make Sure You've confirmed your email."}, status=status.HTTP_401_UNAUTHORIZED)            
    
    # Get Logged in User Details.
    if request.method == 'GET':    
        serializer = CustomUserSerializer(user)
        return JsonResponse(serializer.data)

    # Update Logged in User Details.
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
    
    # Delete Looged in User Account.
    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'Response':'Successfully Deleted Requested Resource.'}, status=status.HTTP_200_OK)


# Reset Password Endpoint
@csrf_exempt
def reset_password(request):
    
    # Data Sanitization
    if not request.method=="POST":
         return JsonResponse({'Error': 'Please Send a POST request with Valid Parameters Only.'},status=status.HTTP_400_BAD_REQUEST)
    
    # Retriving Email and Passwords from POST Data.
    email = request.POST["email"]
    password = request.POST["password"]

    # If User Founds, API Reset's the password & return status 'HTTP_200_OK' else 'HTTP_404_NOT_FOUND'. This Use case implemented using a 'Readable Exception Handling block'
    try:
        current_user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return JsonResponse({"Response":"User Not Found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        current_user.password = password
        current_user.save()
        return HttpResponse(status=status.HTTP_200_OK)
