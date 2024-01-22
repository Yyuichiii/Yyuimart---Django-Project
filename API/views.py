from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from User_Account.models import CustomUser
from API.serializers import User_serializer
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.conf import settings
from User_Account.utils import generateOTP
from User_Account.email import email_otp,email_success_register
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect,csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.

# API View function for Registeration of user
# @method_decorator(csrf_protect, name='dispatch')
class Register_view(APIView):
    # Use SessionAuthentication
    authentication_classes = [SessionAuthentication]  
    # permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer=User_serializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            token=PasswordResetTokenGenerator().make_token(user=user)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            url=reverse('otp', kwargs={'uid':uid,'token':token})
            link = f'{settings.SITE_DOMAIN}/api{url}'
            return Response({'Verification Link':link},status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Otp_view(APIView):
    def get(self,request,uid,token,format=None):
        user=CustomUser.objects.get(id=urlsafe_base64_decode(force_str(uid)))
        if PasswordResetTokenGenerator().check_token(user=user,token=token):
            generated_otp=generateOTP(6)
            email_otp(generated_otp,user.email,user.name)
            request.session['otp_generated']=generated_otp
            print(request.session.get('otp_generated'))
            return Response({"msg":"The email has been sent"},status=status.HTTP_200_OK)
        else:
            user.delete()
            request.session.flush()
            return Response({"msg":"The otp verification window closed!!!"},status=status.HTTP_400_BAD_REQUEST)
        

    def post(self,request,uid,token,format=None):
        user=CustomUser.objects.get(id=urlsafe_base64_decode(force_str(uid)))
        if PasswordResetTokenGenerator().check_token(user=user,token=token):
            if request.data['otp']==request.session.get('otp_generated'):
                user.is_active=True
                user.save()
                email_success_register(user.email,user.name)
                return Response({"msg":"The user has been verified successfully"},status=status.HTTP_201_CREATED)

            else:
                return Response({"msg":"The otp is incorrect!!!"},status=status.HTTP_400_BAD_REQUEST)

        else:
            user.delete()
            request.session.flush()        
        return Response({"msg":"The otp verification window closed!!!"},status=status.HTTP_400_BAD_REQUEST)