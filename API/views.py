from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from User_Account.models import CustomUser,user_address
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.conf import settings
from User_Account.utils import generateOTP
from User_Account.email import email_otp,email_success_register
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from User_Account.email import password_email
from API.serializers import User_serializer,LoginSerializers,User_ProfileSerializer,User_AddressSerializer,PasswordChangeSerializer


# Create your views here.

# function  to generate the token with refresh token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
    }




# API View function for Registeration of user
class Register_view(APIView):

    def post(self, request, format=None):
        serializer=User_serializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            token=PasswordResetTokenGenerator().make_token(user=user)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            url=reverse('otp', kwargs={'uid':uid,'token':token})
            link = f'{settings.SITE_DOMAIN}/api{url}'
            # Generating the link for otp verification and get/post request to the link should be from the same browser for security reasons
            return Response({'Verification Link':link},status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# APIView for generating the otp,email and verifying the otp
class Otp_view(APIView):
    def get(self,request,uid,token,format=None):
        try:
            user=CustomUser.objects.get(id=urlsafe_base64_decode(force_str(uid)))
            if PasswordResetTokenGenerator().check_token(user=user,token=token):
                generated_otp=generateOTP(6)
                email_otp(generated_otp,user.email,user.name)
                request.session['otp_generated']=generated_otp
                print("The otp is :",request.session.get('otp_generated'))
                return Response({"msg":"The email has been sent"},status=status.HTTP_200_OK)
            else:
                request.session.flush()
                return Response({"msg":"The otp verification window closed!!!"},status=status.HTTP_400_BAD_REQUEST)
            
        except:
            return Response({"msg":"Cannot access the Page"},status=status.HTTP_403_FORBIDDEN)
        

    def post(self,request,uid,token,format=None):
        user=CustomUser.objects.get(id=urlsafe_base64_decode(force_str(uid)))
        if PasswordResetTokenGenerator().check_token(user=user,token=token):
            if request.data['otp']==request.session.get('otp_generated'):
                user.is_active=True
                user.save()
                request.session.flush()
                email_success_register(user.email,user.name)
                return Response({"msg":"The user has been verified successfully"},status=status.HTTP_201_CREATED)

            else:
                return Response({"msg":"The otp is incorrect!!!"},status=status.HTTP_400_BAD_REQUEST)

        else:
            user.delete()
            request.session.flush()        
        return Response({"msg":"The otp verification window closed!!!"},status=status.HTTP_400_BAD_REQUEST)
    

# APIView for authenticating the registered user
class LoginView(APIView):
    def post(self, request, format=None):
        serializer=LoginSerializers(data=request.data)
        if serializer.is_valid():
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token},status=status.HTTP_200_OK)

        return Response({'error':'User is not Authenticated'},status=status.HTTP_400_BAD_REQUEST)
    
# APIView for generating the new AccessToken from the refresh token
class Refresh_token_view(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)

            return Response({"access_token": access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# APIView for user profile and making patch request for changing the user profile data
class User_Profile(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
            serializer=User_ProfileSerializer(request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
            
    def patch(self,request,format=None):
        serializer=User_ProfileSerializer(data=request.data,instance=request.user,partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)        
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# APIView for getting the user address and creating/updating the user_addresss
class User_Address_View(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,format=None):
        try:
            user_address_instance = user_address.objects.get(user=request.user)
            serializer = User_AddressSerializer(user_address_instance)
            return Response(serializer.data,status=status.HTTP_200_OK)

        except:
            return Response({"message": "User address not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self,request,format=None):
        user_address_query = user_address.objects.filter(user=request.user)
        if user_address_query.exists():
            return Response({'error':'User Address already Exists'}, status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = User_AddressSerializer(data=request.data)
            if serializer.is_valid():
                user = request.user
                serializer.save(user=user)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request,format=None):
        try:
            user_address_instance = user_address.objects.get(user=request.user)
            serializer = User_AddressSerializer(user_address_instance, data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)  # Ensure the user remains the same
                return Response(serializer.data,status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "User address not found."}, status=status.HTTP_404_NOT_FOUND)
        

# APIView for updating the password
class PasswordChangeView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request,format=None):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password1')

            user = request.user
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                # This is inactive , making the response faster
                # password_email(user.name,user.email)
                return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Incorrect old password."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)