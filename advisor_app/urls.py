"""advisor URL Configuration

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
from django.contrib import admin
from django.urls import include, path
from advisor_app import views
from .api import RegisterApi,LogIn


urlpatterns = [
    path('admin/advisor/', views.Admin, name='Admin'),
    path('user/register/', RegisterApi.as_view()),
    path('user/login/', views.UserLogin),
    path('checklogin/', LogIn.as_view()),
    path('user/<int:user_id>/advisor/', views.GetAdmins, name='GetAdmins'),
    path('user/<int:user_id>/advisor/<int:advisor_id>/', views.BookCall, name='BookCall'),
    path('user/<int:user_id>/advisor/booking/', views.GetCalls, name='GetCalls'),
]