from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
#from django.contrib.auth import login 
#from django.contrib.auth.hashers import make_password, check_password

from rest_framework import status,permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
#from rest_framework.authtoken.serializers import AuthTokenSerializer
from new_app.models import CustomUser
#from knox.models import AuthToken
#from knox.views import LoginView as KnoxLoginView
from new_app.serializers import CustomUserSerializer,CustomUser_loginSerializer,UserSerializer
# from cryptography.fernet import Fernet

@api_view(['POST'])
def loginuser_view(request):
        #serializer = CustomUser_loginSerializer(data=request.data)
        data=request.data
        email=data.get('email')
        password=data.get('password')
        data={}
        if CustomUser.objects.filter(email=email,password=password).exists():
            user=CustomUser.objects.get(email=email,password=password)
            data['response']=1
            data['uid']=user.id
            data['first_name']=user.first_name
            data['middile_name']=user.middile_name
            data['last_name']=user.last_name
            data['email']=user.email
            data['role']=user.role_type
            return Response(data)
        else:
            data['response']=0
            data['error']='User id or password is incorrect!'
            return Response(data)


# Create your views here.
@api_view(['POST'])
def customusercreate_view(request):    
    serializer=CustomUserSerializer(data=request.data)
    data={}
    if serializer.is_valid():
        result=serializer.save()
        data['response']=1
        data['first_name']=result.first_name
        data['middile_name']=result.middile_name
        data['last_name']=result.last_name
        data['email']=result.email
        data['role']=result.role_type
        #data['token']=AuthToken.objects.create(result)[1]
        #data['password']=result.password
        #data=serializer.data
        return Response(data)
    else:
        serializer.errors.setdefault('response',0)     
        return Response(serializer.errors)

@api_view(['GET'])
def userlist_view(request):
    data={}
    try:
        users=CustomUser.objects.all()
        serializer=CustomUserSerializer(users,many=True) 
        data['response']=1
        return Response(serializer.data)
    except:
        data['response']=0
        return Response(data) 


@api_view(['GET'])
def userdetail_view(request,pk):
    data={} 
    try:   
        users=CustomUser.objects.get(id=pk)
        serializer=CustomUserSerializer(users,many=False)
        data['response']=1
        return Response(serializer.data)
    except:   
        serializer.errors['response']=0
        return Response(serializer.errors)
    

@api_view(['PUT'])            
def userupdate_view(request):
    #user_serializer=UserSerializer(data=request.data)
    form_data=request.data
    data={}
    try:
        userid=form_data.get('id')
        user = CustomUser.objects.get(id=userid) 
    except:
        data['response']=0  
        data['error']="Invalid Data Provided"  
        return Response(data) 
    user_serializer=UserSerializer(instance=user,data=request.data) 
    if user_serializer.is_valid():
        result=user_serializer.save() 
        data['response']=1
        data['first_name']=result.first_name
        data['middile_name']=result.middile_name
        data['last_name']=result.last_name
        data['role_type']=result.role_type
        return Response(data) 
    else:
        user_serializer.errors['response']=0
        return Response(user_serializer.errors)    
        #return Response(data) 


@api_view(['POST'])            
def userdelete_view(request):
    form_data=request.data
    data={}
    try:
        userid=form_data.get('id')
        user = CustomUser.objects.get(id=userid) 
        user.delete()
        data['response']=1
        data['message']="User Deleted Successfully"
        return Response(data)
    except:
        data['response']=0
        data['message']="Error Occur While Deleting User"
        return Response(data) 
          
    