from rest_framework.test import APITestCase
from API.serializers import User_serializer
from User_Account.models import CustomUser
from django.urls import reverse

class test_registration_view(APITestCase):
    def test_register(self):
        data={
            "email":"test@gmail.com",
            "name":"test",
            "Phone":"127845469",
            "password1":"t1234est#",
            "password2":"t1234est#"
        }
        response=self.client.post(reverse('api_registration'),data=data)
        self.assertTrue(CustomUser.objects.filter(email=data["email"]).exists())
        self.assertFalse(CustomUser.objects.get(email=data["email"]).is_active)
        self.assertEqual(response.status_code,201)

        # Testing when serializer is not valid
        response=self.client.post(reverse('api_registration'),data=data)
        self.assertEqual(response.status_code,400)


class test_otp_view(APITestCase):
    def test_otp_generation(self):
        data={
            "email":"test@gmail.com",
            "name":"test",
            "Phone":"127845469",
            "password1":"t1234est#",
            "password2":"t1234est#"
        }
        response=self.client.post(reverse('api_registration'),data=data)
        otp_link=response.data['Verification Link']
        
        # Testing the get request 
        response1=self.client.get(otp_link,data=data)
        self.assertEqual(response1.status_code,200)
        # Check for the otp
        self.assertTrue(self.client.session['otp_generated'])
        
        # Test for get request with invalid/expired token
        invalid_token_link='http://localhost:8000/api/otp/MQ/c19edx-6bf8c3c5558c8ef19ea0a63988da/'
        invalid_token_response=self.client.get(invalid_token_link,data=data)
        self.assertEqual(invalid_token_response.data['msg'],'The otp verification window closed!!!')
        self.assertEqual(invalid_token_response.status_code,400)
    
        # Test for get request for random otp link
        random_link='http://localhost:8000/api/otp/random/c19edx-6brandom58c8ef19ea0a63988da/'
        random_response=self.client.get(random_link,data=data)
        self.assertEqual(random_response.data['msg'],'Cannot access the Page')
        self.assertEqual(random_response.status_code,403)


    def test_otp_verification(self):
        data={
            "email":"test@gmail.com",
            "name":"test",
            "Phone":"127845469",
            "password1":"t1234est#",
            "password2":"t1234est#"
        }
        response=self.client.post(reverse('api_registration'),data=data)
        otp_link=response.data['Verification Link'] 
        response1=self.client.get(otp_link,data=data)
        otp=self.client.session['otp_generated']

        data1={
            'otp':otp
        }
        response2=self.client.post(otp_link,data=data1)
        self.assertEqual(response2.data['msg'],'The user has been verified successfully')
        self.assertEqual(response2.status_code,201)
        self.assertTrue(CustomUser.objects.filter(email=data["email"]).exists())

    # Test when something bad happens
class test_invalid(APITestCase):
    def test_otp_verification_error(self):
        data={
            "email":"tet@gmail.com",
            "name":"test",
            "Phone":"127845469",
            "password1":"t1234est#",
            "password2":"t1234est#"
        }
        response=self.client.post(reverse('api_registration'),data=data)
        otp_link=response.data['Verification Link'] 
        response1=self.client.get(otp_link,data=data)
        
        otp=self.client.session['otp_generated']

        data1={
            'otp':'random'
        }
        response2=self.client.post(otp_link,data=data1)
        self.assertEqual(response2.data['msg'],'The otp is incorrect!!!')
        self.assertEqual(response2.status_code,400)
        self.assertFalse(CustomUser.objects.get(email='tet@gmail.com').is_active)

    # Test when invalid/expired Token 
        invalid_token_link='http://localhost:8000/api/otp/MQ/c19edx-6bf8c3c5558c8ef19ea0a63988da/'
        invalid_token_response=self.client.post(invalid_token_link,data=data1)
        self.assertEqual(invalid_token_response.data['msg'],'The otp verification window closed!!!')
        self.assertEqual(invalid_token_response.status_code,400)

