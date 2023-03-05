from django.db import models
# Create your models here.

class CustomUser(models.Model):
    
    userId = models.AutoField(primary_key=True)
   
    full_name = models.CharField(max_length=355)
   
    email = models.EmailField(max_length=50, unique=True ) 
   
    password = models.CharField(max_length=20)
   
    gender = models.CharField(max_length=255, choices=[('Male','Male'),('Female', 'Female'),('Other','Other')])
   
    age = models.IntegerField()
   
    height_cm = models.FloatField()
   
    weight_kg = models.FloatField()

    calculated_BMI = models.FloatField(default=0.0)
   
    is_verified = models.BooleanField(default=False)
   
    is_active=models.BooleanField(default=False)
   
    last_login = models.DateTimeField(null=True)

    session_token = models.CharField(default="", max_length=20,blank=True,null=True)
   
    registered_date = models.DateTimeField(auto_now_add=True)
   
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return  self.full_name
    
    def caculate_BMI(self):
        self.calculated_BMI = self.weight / (self.height/100)**2
    
    
    