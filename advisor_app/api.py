from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from .serializer import RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
import requests
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
#Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        post_data = {"username":request.data["username"],"password":request.data["password"]}
        response = requests.post('http://localhost:8000/api/token/', data=post_data)
        print(self.get_serializer_context())
        return Response({
            "token":response.content,
            "user": UserSerializer(user,context=self.get_serializer_context()).data,
        })

class LogIn(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        content = {'message': 'Successfully Logged In!'}
        return Response(content)