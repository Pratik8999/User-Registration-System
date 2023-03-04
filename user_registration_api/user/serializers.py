from rest_framework.serializers import ModelSerializer
from .models import CustomUser


# To represent or share the Python class - 'CustomUser' instances in a readable 
# and universally used data-sharing format JSON.

# Using Serializers we're converting each 'CustomUser' object into its equivalent JSON Format.
# We can also apply various 'validation methods' (Validators) to check the validity of an object attributes.
class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser

        read_only_fields = ('userId','is_verified','is_active','last_login','registered_date','modified_date', 'session_token')
        
        extra_kwargs = {'password' : {'write_only':True} }
        
        fields = '__all__'

class LoginSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        extra_kwargs = {'password' : {'write_only':True} }
        fields = ['email',]


# either we can create a new instance & save it in db or we can get the instance from db.

#  OBJECT 1
# pratik = CustomUser.objects.get(pk=1)
# pratik   


#  OBJECT 2
# sachin_sir = CustomUser.objects.get(pk=2)
# sachin_sir


# The django model serialization has two phases

# 1. Convert the object into native Python datatype (<class Dict>) as per the implemented instructions in the 'serializers.py' for that model.

# 2. Convert the natively serialized object (<class Dict>) into actual JSON data type. 

# *Note: the step '2' converts data into JSON but in its 'binary form' so that the reciever can deserialize the JSON 
#        'bytes' to its actual 'String' representation


# Step 1 : Converting the Model object into native python datatype (<class Dict>) as dictonary closely resembles to JSON.

# native_data = CustomUserSerializer(CustomUser)

#  print("Output:",native.data)
#  Output: {'userId': 1, 'full_name': 'Pratik Joshi', 'email': 'joshipratik8999@gmail.com', 'gender': 'Male', 
#           'age': 24, 'height': 5.3, 'weight': 67.0, 'calculated_BMI': 0.0, 'is_verified': False, 'is_active': False,
#           'last_login': '2023-03-04T10:42:01.822260'}



# Step 2 : Converting the nativly serialized object into Actual JSON but in its binary format.

# actual_json = JSONRenderer().render(json_data_of_pratik.data)
# print(actual_json
# b'{"userId":1,"full_name":"Pratik Joshi","email":"joshipratik8999@gmail.com","gender":"Male","age":24,
#    "height":5.3,"weight":67.0,"calculated_BMI":0.0,"is_verified":false,"is_active":false,
# "last_login":"2023-03-04T10:42:01.822260"}'

# type(actual_json)

# <class 'bytes'>


# Now let's briefly look at the deserialization process.

# import io
# 
# byte_stream = io.BytesIO(actual_json)
# print("Output:",byte_stream)
# Output: <_io.BytesIO object at 0x000001FE2C1B9530>

# ** Actual Deserialiaztion of JSON Binary to native python datatype  (<class Dict>)

# deseralized_data = JSONParser().parse(byte_stream)
# deseralized_data
# {'userId': 1, 'full_name': 'Pratik Joshi', 'email': 'joshipratik8999@gmail.com', 'gender': 'Male', 'age': 24,
#  'height': 5.3, 'weight': 67.0, 'calculated_BMI': 0.0, 'is_verified': False, 'is_active': False,
#  'last_login': '2023-03-04T10:42:01.822260'}

