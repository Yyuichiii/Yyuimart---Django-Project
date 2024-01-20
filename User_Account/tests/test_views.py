from django.test import TestCase
from User_Account.models import CustomUser
from User_Account.forms import User_Reg,otp_form
from django.urls import reverse
import pdb

class home_test(TestCase):
    def test_home_view(self):
        admin=CustomUser.objects.create_superuser(email="test@gmail.com",password="test1234")
        self.client.login(email="test@gmail.com",password="test1234")
        # Check if admin is login
        self.assertTrue('_auth_user_id' in self.client.session)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertFalse('_auth_user_id' in self.client.session)
        self.assertTrue('product' in response.context)


class registeration(TestCase):
    def test_registration_view(self):
        response = self.client.get(reverse('registration'))
        self.assertTrue('form' in response.context)
        post_data = {
            'email': 'test@gmail.com',
            'name': 'ndrd',
            'Phone': '123456789',
            'password1': 'test1234#',
            'password2': 'test1234#',
        }
        response = self.client.post(reverse('registration'),data=post_data)
        form = User_Reg(data=post_data)
        self.assertTrue(form.is_valid())
        self.assertTrue('ue' in self.client.session)
        self.assertEqual(self.client.session['ue'], "test@gmail.com")
        self.assertEqual(response.status_code, 302)

        # After form.is_valid() , request redirects to the otpfun 
        response = self.client.get(reverse('otp'),HTTP_REFERER='otp')
        self.assertEqual(self.client.session['ue'], "test@gmail.com")
        self.assertTrue('otp_generated' in self.client.session)
        self.assertIsInstance(response.context['form'], otp_form)
        self.assertNotEqual(response.status_code, 302)
        print(self.client.session['otp_generated'])





        data1={'otp_digit':self.client.session['otp_generated']}


        response_post=self.client.post(reverse('otp'),HTTP_REFERER='otp')
        form2=otp_form(data=data1)
        form2.is_valid()
        # pdb.set_trace()
        self.assertTrue(form2.is_valid())
        # self.assertTrue(CustomUser.objects.filter(email='test@gmail.com').exists())
        # pdb.set_trace()
        # self.assertEqual(response_post.status_code, 302)
        

    def test_otp_verfication(self):
        data2={'otp_digit':'123456'}
        response_post=self.client.post(reverse('otp'),HTTP_REFERER='otp')
        form2=otp_form(data=data2)
        form2.is_valid()
        form2.is_valid()
        # pdb.set_trace()



