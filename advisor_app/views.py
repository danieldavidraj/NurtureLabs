from django.shortcuts import render
from django.http import HttpResponse
from advisor_app.forms import AddAdvisor,RegisterUser,BookCallTime,UserLoginInfo
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from django.contrib.auth.models import User

advisors=[]

@csrf_exempt
def Admin(request):
   if request.method == "POST":
      AddAdvisorForm = AddAdvisor(request.POST)
      if AddAdvisorForm.is_valid():
         Advisor_name = AddAdvisorForm.cleaned_data['Advisor_name']
         Advisor_Photo_URL = AddAdvisorForm.cleaned_data['Advisor_Photo_URL']
         advisors.append({"id":len(advisors)+1,"Advisor_name":Advisor_name,"Advisor_Photo_URL":Advisor_Photo_URL})
         return HttpResponse(status=200)
      else:
         return HttpResponse("fields are missing",status=400)

@csrf_exempt
def GetAdmins(request,user_id):
   if request.method == "GET":
      return HttpResponse(advisors,status=200)

bookings=[]

@csrf_exempt
def UserLogin(request):
   if request.method == "POST":
      UserLoginInfoForm = UserLoginInfo(request.POST)
      if UserLoginInfoForm.is_valid():
         email = UserLoginInfoForm.cleaned_data['email']
         password = UserLoginInfoForm.cleaned_data['password']
         all_users = User.objects.values()
         for item in all_users:
            if item['email'] == email:
               username=item["username"]
               user_id=item["id"]
               break
         else:
            return HttpResponse("email/password combination was wrong",status=401)
         post_data = {"username":username,"password":password}
         response = requests.post('http://localhost:8000/api/token/', data=post_data)
         if response.status_code!=200:
            return HttpResponse(response.text,status=response.status_code)
         else:
            return HttpResponse(response.text+'{"user_id":'+str(user_id)+'}',status=response.status_code)
            # headers = {"Authorization": "Bearer "+json.loads(response.content)["access"]}
            # response = requests.post('http://localhost:8000/checklogin/',headers=headers)
            # return HttpResponse(response,status=response.status_code)
      else:
         return HttpResponse("fields are missing",status=400)

@csrf_exempt
def BookCall(request,user_id,advisor_id):
   if request.method == "POST":
      all_users = User.objects.values()
      for item in all_users:
         if item['id'] == user_id:
            BookCallTimeForm = BookCallTime(request.POST)
            if BookCallTimeForm.is_valid():
               booking_time = BookCallTimeForm.cleaned_data['Booking_time']
               for item in advisors:
                  if item['id'] == advisor_id:
                     bookings.append({
                     "User_Id":user_id,
                     "Advisor_Name":item["Advisor_name"],
                     "Advisor_Profile_Pic":item["Advisor_Photo_URL"],
                     "Advisor_Id":advisor_id,
                     "Booking_time":booking_time,
                     "Booking_id":len(bookings)+1,
                     })
                     return HttpResponse(status=200)
               else:
                  return HttpResponse("No advisor with {id}".format(id=advisor_id),status=400)
            else:
               return HttpResponse("fields are missing",status=400)
      else:
         return HttpResponse("No user with {id}".format(id=user_id),status=400)
         
@csrf_exempt
def GetCalls(request,user_id):
   if request.method == "GET":
      all_users = User.objects.values()
      for item in all_users:
         if item['id'] == user_id:
            response=[]
            for item in bookings:
               if item['User_Id'] == user_id:
                  response.append(item)
            if(response):
               return HttpResponse(response)
            else:
               return HttpResponse("No bookings for user with id {id}".format(id=user_id),status=400)
      else:
         return HttpResponse("No user with id {id}".format(id=user_id),status=400)   
         
         