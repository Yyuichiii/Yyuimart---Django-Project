from rest_framework.test import APITestCase
from API.serializers import User_serializer
from User_Account.models import CustomUser,user_address
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

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

class test_login_view(APITestCase):
    def test_login(self):
        user=CustomUser.objects.create_user(email="test@gmail.com",name="test",Phone="127845469",
            password="t1234est#")
        user.save()
        post_data={
            "email":"test@gmail.com",
            "password":"t1234est#"
        }
        response=self.client.post(reverse('api_login'),data=post_data)
        self.assertEqual(response.status_code, 200)
        # Check if the token is generated in the response
        self.assertIn('token', response.data)


    def test_login_invalid(self):
        user=CustomUser.objects.create_user(email="test@gmail.com",name="test",Phone="127845469",
            password="t1234est#")
        user.save()
        post_data={
            "email":"test@gmail.com",
            "password":"1234est#"
        }
        response=self.client.post(reverse('api_login'),data=post_data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.data)

        post_data_invalid={
            "email":"",
            "password":""
        }

        response1=self.client.post(reverse('api_login'),data=post_data_invalid)
        self.assertEqual(response1.status_code, 400)

class TestRefreshTokenView(APITestCase):
    def test_refresh_token(self):
        user=CustomUser.objects.create_user(email="test@gmail.com",name="test",Phone="127845469",
            password="t1234est#")
        user.save()
        post_data={
            "email":"test@gmail.com",
            "password":"t1234est#"
        }
        response_generate_token=self.client.post(reverse('api_login'),data=post_data)

        # Assume you have a valid refresh token
        valid_refresh_token = response_generate_token.data['token']['refresh_token']

        # Make a POST request to the refresh token endpoint
        post_data = {
            "refresh_token": valid_refresh_token
        }
        response = self.client.post(reverse('api_refreshtoken'), data=post_data)

        # Check if the response is HTTP 200 OK
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the access token
        self.assertIn('access_token', response.data)

    def test_refresh_token_invalid(self):
        # Make a POST request to the refresh token endpoint
        post_data = {
            "refresh_token": ""
        }
        response = self.client.post(reverse('api_refreshtoken'), data=post_data)

        # Check if the response is HTTP_406_NOT_ACCEPTABLE
        self.assertEqual(response.status_code, 406)
        self.assertIn('error', response.data)


        post_data = {
            "refresh_token": "15163135fjlrandomtoken"
        }
        response = self.client.post(reverse('api_refreshtoken'), data=post_data)

        # Check if the response is HTTP_400_BAD_REQUEST
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)

class TestUserProfileView(APITestCase):
    def test_get_user_profile(self):
        user=CustomUser.objects.create_user(email="test@gmail.com",name="test",Phone="127845469",
            password="t1234est#")
        user.save()

        # Create refresh and access tokens for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        url = reverse('api_profile')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # Check if the response is HTTP 200 OK
        self.assertEqual(response.status_code, 200)

    def test_update_user_profile(self):
        user=CustomUser.objects.create_user(email="test@gmail.com",name="test",Phone="127845469",password="t1234est#")
        user.save()

        # Create refresh and access tokens for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        url = reverse('api_profile')
        data = {'name': 'updated_name'}
        response = self.client.patch(url, data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
    #     # Check if the response is HTTP 200 OK
        self.assertEqual(response.status_code, 200)


class TestUserAddressView(APITestCase):

    def test_get_user_address(self):
        user=CustomUser.objects.create_user(email="test@gmail.com",name="test",Phone="127845469",
            password="t1234est#")
        user.save()

        # Create a user address instance for the test user
        address = user_address.objects.create(
            user=user,
            Name="test_Name",
            Phone="123456789",
            Pincode="123456",
            State="Rajasthan",
            house_no="232dsdgfg",
            Road_name="dsjktest"
        )
        address.save()

        # Create refresh and access tokens for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        url = reverse('api_address')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # Check if the response is HTTP 200 OK
        self.assertEqual(response.status_code, 200)


        # if Address does not exists
        address.delete()
        response1 = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # Check if the response is HTTP_404_NOT_FOUND
        self.assertEqual(response1.status_code, 404)
        self.assertIn('error',response1.data)

    def test_post_user_address(self):
        user=CustomUser.objects.create_user(email="test@gmail.com",name="test",Phone="127845469",
            password="t1234est#")
        user.save()
        # Create refresh and access tokens for the user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        url = reverse('api_address')
        data={
        "Name":"test_Name",
        "Phone":"123456789",
        "Pincode":"123456",
        "State":"Rajasthan",
        "house_no":"232dsdgfg",
        "Road_name":"dsjktest"
        }
        
        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
    #Check if the response is HTTP 201 Created
        self.assertEqual(response.status_code, 201)

    # if Address already exists

        response1 = self.client.post(url, data=data, format='json', HTTP_AUTHORIZATION=f'Bearer {access_token}')

        #Check if the response is HTTP_400_BAD_REQUEST
        self.assertEqual(response1.status_code, 403)

    # def test_put_user_address(self):
    #     url = reverse('user_address')
    #     data = {'address': 'Updated Address', 'city': 'Updated City', 'country': 'Updated Country'}
    #     request = self.factory.put(url, data, format='json', HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    #     response = User_Address_View.as_view()(request)
        
    #     # Check if the response is HTTP 200 OK
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)