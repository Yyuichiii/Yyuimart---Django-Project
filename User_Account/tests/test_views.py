from django.test import TestCase
from User_Account.models import CustomUser
from User_Account.forms import User_Reg,otp_form
from django.urls import reverse
import pdb

class home_test(TestCase):
    def test_home_view(self):
        # Created an admin for testing
        admin=CustomUser.objects.create_superuser(email="test@gmail.com",password="test1234")
        # Login the Admin
        self.client.login(email="test@gmail.com",password="test1234")
        # Check if admin is login
        self.assertTrue('_auth_user_id' in self.client.session)

        # Making get request
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Check if admin is logout usinn admin_logout function in home view
        self.assertFalse('_auth_user_id' in self.client.session)
        # checking for the context return
        self.assertTrue('product' in response.context)
        # checking for the correct html render
        self.assertTemplateUsed(response, 'User_Account/home.html')


class registration_test(TestCase):
    def test_registration_view(self):
        # Checking get request with user authenticated
        user=CustomUser.objects.create(email="test@gmail.com",password="test1234")
        self.client.force_login(user=user)
        response_with_user_login = self.client.get(reverse('registration'))
        self.assertTemplateUsed('User_Account/home.html')
        self.assertEqual(response_with_user_login.status_code,302)
        self.client.logout()

        # Checking if get request with user not authenticated
        response = self.client.get(reverse('registration'))
        self.assertTrue(response.status_code,200)
        self.assertTrue('form' in response.context)
        self.assertTemplateUsed('User_Account/customerregistration.html')

        # Checking with post request
        post_data = {
            'email': 'tesstttt@gmail.com',
            'name': 'ndrd',
            'Phone': '123456789',
            'password1': 'test1234#',
            'password2': 'test1234#',
        }
        response = self.client.post(reverse('registration'),data=post_data,follow=False)
        user_inactive=CustomUser.objects.get(email=post_data['email'])
        # Checking if the user is active or not
        self.assertFalse(user_inactive.is_active)
        self.assertEqual(response.status_code,302)
        self.assertTemplateNotUsed('User_Account/customerregistration.html')


    def test_otp_generation(self):
        # Test for generating otp for inactive user using the get request
        post_data = {
            'email': 'tesstttt@gmail.com',
            'name': 'ndrd',
            'Phone': '123456789',
            'password1': 'test1234#',
            'password2': 'test1234#',
        }
        response = self.client.post(reverse('registration'),data=post_data,follow=True)
        self.assertEqual(response.status_code,200)
        self.assertTrue("form" in response.context)
        self.assertTrue('otp_generated' in self.client.session)
        self.assertTemplateUsed('User_Account/otp.html')


    def test_otp_verification(self):
        # Test for verifing otp for inactive user using the post request and making the user active
        post_data = {
            'email': 'tesstttt@gmail.com',
            'name': 'ndrd',
            'Phone': '123456789',
            'password1': 'test1234#',
            'password2': 'test1234#',
        }
        # Making post request to the registration so it can generate the redirect dynamic link for otp verification process
        response = self.client.post(reverse('registration'),data=post_data,follow=False)
        # Making get request to the  generated url to get the generated otp in the session 
        response1=self.client.get(response.url)
        

        # Passing the random otp to the data which will be sent to the post request to the url of otp verification
        otp_data={
            'otp_digit':'random'
        }
        # making the post request to the otp verification with incorrect otp passed through the post data
        response2=self.client.post(response.url,data=otp_data)
        # If the otp is incorrrect the request return back to the otp verfication form page
        self.assertEqual(response2.status_code,200)
        self.assertTemplateUsed('User_Account/otp.html')
        user=CustomUser.objects.get(email=post_data['email'])
        self.assertFalse(user.is_active)


        # Passing the generated otp to the data which will be sent to the post request to the url of otp verification
        otp_data={
            'otp_digit':self.client.session['otp_generated']
        }
        # finally making the post request to the otp verification with correct otp passed through the post data
        response3=self.client.post(response.url,data=otp_data)
        # If the otp verification get successfully , the request redirects to the login page
        self.assertEqual(response3.status_code,302)
        self.assertTemplateUsed('User_Account/login.html')
        user=CustomUser.objects.get(email=post_data['email'])
        self.assertTrue(user.is_active)
    
    
        # If someone makes a random url , it will redirect it to the home page 
        dynamic_part = "test/testqweweres/"
        random_url = f"/otp/{dynamic_part}"
        expected_response=self.client.get(random_url)
        self.assertEqual(response.status_code,302)
        self.assertTemplateUsed('User_Account/home.html')

    def test_token_invalid(self):
        post_data = {
            'email': 'tesstttt@gmail.com',
            'name': 'ndrd',
            'Phone': '123456789',
            'password1': 'test1234#',
            'password2': 'test1234#',
        }
        # Making post request to the registration so it can generate the redirect dynamic link for otp verification process
        response = self.client.post(reverse('registration'),data=post_data,follow=False)
        # Making get request to the  generated url(otp verification) to retrieve the generated otp in the session 
        response1=self.client.get(response.url)
        t=response.url.split('/')
        uid=t[-3]
        # Generated an url with token which is either invalid/incorrect or expired
        custumer_url=reverse('otp',kwargs={'uid':uid,'token':'randomtoken'})
        otp_data={
            'otp_digit':self.client.session['otp_generated']
        }
        # finally making the post request to the otp verification with correct otp passed but wrong token through the post data
        response3=self.client.post(custumer_url,data=otp_data)
        # This will redirect the view to register and the user will be deleted
        self.assertTemplateUsed('User_Account/registration.html')
        self.assertFalse(CustomUser.objects.filter(email=post_data['email']).exists())




        




        
        

    



    