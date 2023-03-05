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

    # Implemented for easy BMI Analysis Report Generation.
    def BMI_Analyser(self,BMI):
        if BMI <= 18.4:
            return  "You are underweight.\nAdvice: Gain Some More Weight Buddy. Eat Healthy food minimum 4 times a day."
        elif BMI <= 24.9:
            return  "You are absolutely healthy, so Keep Going :)"
        elif BMI <= 29.9:
            return  "You are over weight.\nAdvice: Please daily do some exercise you'll be fine after few days."
        elif BMI <= 34.9:
            return  "You are severely over weight. \nAdvice: Please daily do some exercise you'll be fine after few days."
        elif BMI <= 39.9:
            return  "You are obese.\nAdvice: Please Strictly do some exercises likes running,cycling,walking for some weeks. You'll get better results."
        else:
            return  "You are severely obese.\n Advice: Please immediately Consult a dietitian and Gym Trainer as you've reached the risk BMI levels. If you follow their guidelines you'll be reach back to healthy bmi ratio."

    
    
    