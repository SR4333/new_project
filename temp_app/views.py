from django.shortcuts import render
from django.http import HttpResponse
from temp_app.models import book,Country
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from temp_app.permissions import MyPermission
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissionsOrAnonReadOnly,IsAuthenticatedOrReadOnly,IsAdminUser,AllowAny,DjangoModelPermissions
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication,SessionAuthentication




from .serializers import bookSerializer,CountrySerializer

# Create your views here.
class BookListView(APIView):
    def get(self,request):
        res=book.objects.all()
        serializer=bookSerializer(res,many=True)
        data_dict={'data':serializer.data,'success':"List of Books"}
        return Response(data_dict)

    def post(self,request):
        serializer=bookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data_dict={'data':serializer.data,'success':"Book Created"}
            return Response(data_dict)    
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class BookDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return book.objects.get(pk=pk)
        except book.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = bookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = bookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class BlogPostList_View(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=book.objects.all()
    serializer_class=bookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)   

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    


class BlogDetail_View(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset=book.objects.all()
    serializer_class=bookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)     

class BookList(generics.ListCreateAPIView):
    queryset = book.objects.all()
    serializer_class = bookSerializer

class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = book.objects.all()
    serializer_class = bookSerializer

class BookModelViewSet(viewsets.ModelViewSet):
    queryset=book.objects.all()
    serializer_class=bookSerializer
    authentication_classes=[BasicAuthentication]
    permission_classes=[IsAuthenticated]


class CountryModelViewSet(viewsets.ModelViewSet):
    queryset=Country.objects.all()
    serializer_class=CountrySerializer
    authentication_classes=[SessionAuthentication]
    #permission_classes=[IsAuthenticated]
    #permission_classes=[IsAdminUser]
    #permission_classes=[AllowAny]
    #permission_classes=[IsAuthenticatedOrReadOnly]
    #permission_classes=[DjangoModelPermissions]
    #permission_classes=[DjangoModelPermissionsOrAnonReadOnly]
    permision_classes=[MyPermission]
    




