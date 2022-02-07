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

@api_view(['POST'])
def loginuser_view1(request):
        #serializer = CustomUser_loginSerializer(data=request.data)
        data=request.data
        email=data.get('email')
        password=data.get('password')
        b_password=bytes(password,'utf-8') 
        
        data={}
        
        user= CustomUser.objects.get(email=email)
        pwd=user.password
        key=Fernet.generate_key()
        f = Fernet(key)
        print(pwd)
        decrypted_pwd = f.decrypt(pwd)
        print(decrypted_pwd)
        if b_password == decrypted_pwd:    
                data['response']="Successfully registered a new user"
                data['uid']=user.id
                data['first_name']=user.first_name
                data['middile_name']=user.middile_name
                data['last_name']=user.last_name
                data['email']=user.email
                data['role']=user.role_type
               
                return Response(data)
        else:
                 data['status']="You have entered invalid data"
                 return Response(data)   
        '''except:
            data['status']="You have entered invalid data"
            return Response(data) 
        if CustomUser.objects.filter(email=email,password=pwd).exists():
            user=CustomUser.objects.get(email=email,password=pwd)
            data['response']="Successfully registered a new user"
            data['uid']=user.id
            data['first_name']=user.first_name
            data['middile_name']=user.middile_name
            data['last_name']=user.last_name
            data['email']=user.email
            data['role']=user.role_type
            data['status']="Login Successfully"
            return Response(data)
        else:
            data['status']="You have entered invalid data"
            return Response(data) '''   


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
    else:
        data['response']=0
        data['error']="some error happens"
        data=serializer.errors        
    return Response(data)

@api_view(['GET'])
def userlist_view(request):
    try:
        users=CustomUser.objects.all()
        serializer=CustomUserSerializer(users,many=True) 
    except:
        serializer.data="Error occur while Fecthing Data." 
    return Response(serializer.data) 


@api_view(['GET'])
def userdetail_view(request,pk): 
    try:   
        users=CustomUser.objects.get(id=pk)
        serializer=CustomUserSerializer(users,many=False)
    except:   
        #serializer=register_usersSerializer(users,many=False)
        serializer.data=0
    return Response(serializer.data)
    
'''@api_view(['PUT'])
def userupdate_view(request,pk):
            data={}
            #try:
            user=CustomUser.objects.get(id=pk)
            serializer=CustomUserSerializer(instance=user,data=request.data)
            if serializer.is_valid():
                serializer.save()
                print("hello")
                data['response']=1
            return Response(data) 
            except:
            data['response']=0
            return Response(data)''' 

'''@api_view(['PUT'])            
def userupdate_view(request,pk):
    try:
        user=CustomUser.objects.get(id=pk)
        serializer=CustomUserSerializer(instance=user,data=request.data)
        print("try")
        if serializer.is_valid():
            serializer.save()
            print("hello")
    except:
         serializer.data="Error occur while Fecthing Data."
         print("except")   
    
    return Response(serializer.data) '''       
@api_view(['PUT'])            
def userupdate_view(request,pk):
    data={}
    try: 
        user = CustomUser.objects.get(pk=pk) 
    except:
        data['response']=0
        return Response(data)   
    user_data = JSONParser().parse(request) 
    user_serializer = UserSerializer(user, data=user_data) 
    if user_serializer.is_valid():
        result=user_serializer.save() 
        data['response']=1
        data['first_name']=result.first_name
        data['middile_name']=result.middile_name
        data['last_name']=result.last_name
        data['email']=result.email
        data['role_type']=result.role_type
        #return JsonResponse(user_serializer.data) 
    else:
        data['response']=0
    #return JsonResponse(user_serializer.data)    
    return Response(data) 





@api_view(['DELETE'])
def userdelete_view(request,pk):
    data={}
    try:
        user=CustomUser.objects.get(id=pk)
        serializer=CustomUserSerializer(instance=user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            data['response']=1
    except:
         serializer.data="Error occur while Fecthing Data." 
         serializer.data=0
    
    return Response(serializer.data)         


