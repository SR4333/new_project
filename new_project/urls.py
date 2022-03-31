"""new_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from argparse import Namespace
from posixpath import basename
from django.contrib import admin
from django.urls import path,include
from new_app import views 
from temp_app.views import BookListView,BookDetail,BlogPostList_View,BlogDetail_View,BookDetail,BookList,BookModelViewSet,CountryModelViewSet
from rest_framework.routers import DefaultRouter
#from new_app.views import LoginAPI
#from knox import views as knox_views
router=DefaultRouter()

router.register('books',BookModelViewSet,basename='book')
router.register('country',CountryModelViewSet,basename="country")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_create/',views.customusercreate_view,name='user_create'),
    path('login/', views.loginuser_view, name='login'),
    path('user_list/',views.userlist_view, name='user_list'),
    path('user_detail/<str:pk>/',views.userdetail_view,name="user_detail"),
    path('user_update/',views.userupdate_view,name="user_update"),
    path('user_delete/',views.userdelete_view,name="user_delete"),
    path('book/',BookListView.as_view(),name="book"),
    path('bookdetail/<int:pk>/',BookDetail.as_view(),name="bookdetail"),
    path('booklist/',BlogPostList_View.as_view(),name="booklist"),
    path('bookview/<int:pk>/',BlogDetail_View.as_view(),name="bookview"),
    path('booklist1/',BookList.as_view(),name="booklist1"),
    path('bookview1/<int:pk>',BookDetail.as_view(),name="bookview1"),
    #path('books/',BookModelViewSet,name="books"),
    #path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('',include(router.urls)),
    path('auth/', include('rest_framework.urls',namespace="rest_framework")),
]
