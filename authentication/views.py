from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status, response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, CreateUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from authentication.authentication import BearerTokenAuthentication

User = get_user_model()


class SignupView(generics.CreateAPIView):

 def post(self, request, *args, **kwargs):
        
        user = User.objects.filter(email=request.data.get('email')).first()
        
        if user:    
            return response.Response({'detail': 'Email is already taken'}, status=status.HTTP_400_BAD_REQUEST)    
        
        user = User.objects.create(
            email=request.data.get('email'),
            first_name=request.data.get('email'),
            last_name=request.data.get('email'),
            username=request.data.get('email'),
        )

        user.set_password(request.data.get("password"))
        user.save()

        # delete all previous tokens
        Token.objects.filter(user=user).delete()
        
        # create a new token for that user
        token = Token.objects.create(user=user)
        
        data = dict()
        data['user'] = UserSerializer(user).data
        data['token'] = token.key
        
        return response.Response(data, status=status.HTTP_201_CREATED)
    

# Create your views here.
class LoginView(generics.CreateAPIView):
    
    def post(self, request, *args, **kwargs):
        
        # TODO:
        # add validation to ensure email and password are provided
        # in the post body
        
        
        user = get_object_or_404(User, email=request.data.get('email'))
        
        # if the user is not active throw error
        if not user.is_active:    
            return response.Response({'detail': 'authentication failed'}, status=status.HTTP_400_BAD_REQUEST)    
        
        # if password does not match 
        if not user.check_password(request.data.get('password')):
            return response.Response({'detail': 'invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)    
        
        # delete all previous tokens
        Token.objects.filter(user=user).delete()
        
        # create a new token for that user
        token = Token.objects.create(user=user)
        
        data = dict()
        data['user'] = UserSerializer(user).data
        data['token'] = token.key
        
        return response.Response(data, status=status.HTTP_201_CREATED)
    

class LogoutView(generics.CreateAPIView):
    
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        tokens = Token.objects.filter(user=request.user)
        # delete all tokens affiliated with this user
        tokens.delete()
        return response.Response({'detail': 'Logout Successful'}, status=status.HTTP_200_OK)
