from django import forms

class AddAdvisor(forms.Form):
    Advisor_name = forms.CharField(max_length = 100)
    Advisor_Photo_URL = forms.CharField(max_length = 1000)

class RegisterUser(forms.Form):
    Name = forms.CharField(max_length = 100)
    Email = forms.CharField(max_length = 100)
    Password = forms.CharField(widget = forms.PasswordInput())

class BookCallTime(forms.Form):
    Booking_time = forms.CharField(max_length = 100)

class UserLoginInfo(forms.Form):
    email = forms.CharField(max_length = 100)
    password = forms.CharField(widget = forms.PasswordInput())
