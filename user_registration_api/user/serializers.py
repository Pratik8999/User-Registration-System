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

    def caculate_BMI(self,weight_kg, height_cm):
        return weight_kg / (height_cm/100)**2