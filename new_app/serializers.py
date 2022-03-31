import re
#from django.core.validators import email_re
from django.contrib.auth.hashers import make_password, check_password
# from cryptography.fernet import Fernet

from rest_framework import serializers
from new_app.models import CustomUser
from temp_app.models import book
class CustomUser_loginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email','password')

class CustomUserSerializer(serializers.ModelSerializer):
    books = serializers.PrimaryKeyRelatedField(many=True, queryset=book.objects.all())



    email=serializers.CharField(max_length=255,min_length=4)
    first_name=serializers.CharField(max_length=50,min_length=3)
    #last_name=serializers.CharField(max_length=50,min_length=3)
    #middile_name=serializers.CharField(max_length=50,min_length=3) 
    
   
    # password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=CustomUser
        fields=('id','first_name','last_name','middile_name','email','password','role_type','books')
        # extra_kwargs={'password2':{'write_only':True}}  

    def validate(self,attrs):
        if CustomUser.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({'email', ("Email Already in use")})
        return super().validate(attrs)    


    def save(self):
        #pwd=make_password(self.validated_data['password'])
        #password=self.validated_data['password'].encode()
        password=self.validated_data['password']
        #key=Fernet.generate_key()
        #f = Fernet(key)
        #encrypted_pwd = f.encrypt(password)
        user=CustomUser(
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            middile_name=self.validated_data['middile_name'],
            email=self.validated_data['email'],
            password=password,
            role_type=self.validated_data['role_type']) 
        first_name=self.validated_data['first_name'] 
        last_name=self.validated_data['last_name'] 
        middile_name=self.validated_data['middile_name'] 
        email=self.validated_data['email']
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        password=self.validated_data['password'] 
        # password2=self.validated_data['password2']
        role_type=self.validated_data['role_type']
        pat = re.compile(r"^[a-zA-Z_.]+( [a-zA-Z_.]+)*$")
        if not re.fullmatch(pat, first_name) or first_name.startswith(".") or first_name.startswith("_"):
            raise serializers.ValidationError({'FirstName':"Please Enter valid Data"})
        elif not re.fullmatch(pat, last_name) or last_name.startswith(".") or last_name.startswith("_"):
            raise serializers.ValidationError({'LastName':"Please Enter valid Data"}) 
        elif not re.fullmatch(pat, middile_name) or middile_name.startswith(".") or middile_name.startswith("_"):
            raise serializers.ValidationError({'LastName':"Please Enter valid Data"}) 
        elif not re.fullmatch(regex, email):
            raise serializers.ValidationError({'Email':_("Invalid EmailId")})
                

     
            
        # elif password!=password2:
        #     raise serializers.ValidationError({'Password':"Passwords must match"}) 
        user.set_password(password)    
        user.save()  
        return user  

class UserSerializer(serializers.ModelSerializer):
    #email=serializers.CharField(max_length=255,min_length=4)
    first_name=serializers.CharField(max_length=50,min_length=3)
    last_name=serializers.CharField(max_length=50,min_length=3)
    #middile_name=serializers.CharField(max_length=50,min_length=3)
    role_type=serializers.CharField(max_length=50,min_length=3)
    class Meta:
        model = CustomUser
        fields=('id','first_name','middile_name','last_name','role_type')

    def validate(self,attrs):
        return super().validate(attrs) 