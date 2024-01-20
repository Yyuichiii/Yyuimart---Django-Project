from User_Account.forms import User_Reg,login_form,custom_password_change,address_form,otp_form
from django.test import TestCase
from User_Account.models import CustomUser
import pdb
class User_Creation_form_test(TestCase):
    def test_form_exist(self):
        data={"name":"Test",'email':"test@gmail.com","Phone":"123456789","password1":"test1234#","password2":"test1234#"}
        form=User_Reg(data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_email(self):
        data={"name":"Test",'email':"testgmail.com","Phone":"123456789","password1":"test1234#","password2":"test1234#"}
        form=User_Reg(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)



class Login_form_test(TestCase):
    def test_form_exist(self):
        user=CustomUser.objects.create_user(email="test@gmail.com",password="test1234#",name="test",Phone="123456789")
        data={'email':"test@gmail.com","password":"test1234#"}
        form=login_form(data=data)
        self.assertTrue(form.is_valid())
        
    def test_check_Valid_invalid(self):
        user=CustomUser.objects.create_user(email="test@gmail.com",password="test1234#",name="test",Phone="123456789")
        data={'email':"test@gmail.com","password":"mismatchpassword"}
        form=login_form(data=data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.non_field_errors)

class password_change_form(TestCase):
    def test_form(self):
        user=CustomUser.objects.create_user(email="test@gmail.com",password="test1234#",name="test",Phone="123456789")
        data={"old_password":"test1234#","new_password1":"test1234#","new_password2":"ttest1234#"}
        form=custom_password_change(user,data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('The two password fields didn’t match.',form.errors['new_password2'])
        data1={"old_password":"est1234#","new_password1":"test1234#","new_password2":"test1234#"}
        form1=custom_password_change(user,data=data1)
        self.assertFalse(form1.is_valid())
        self.assertIn("Your old password was entered incorrectly. Please enter it again.",form1.errors['old_password'])
        
        form.save()
        self.assertTrue(user.check_password("test1234#"))
        self.assertFalse(user.check_password("ttest1234#"))

    def test_password_change(self):
        user=CustomUser.objects.create_user(email="test@gmail.com",password="test1234#",name="test",Phone="123456789")
        data={"old_password":"test1234#","new_password1":"ttest1234#","new_password2":"ttest1234#"}
        form=custom_password_change(user,data=data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(user.check_password("ttest1234#"))

class address_form_test(TestCase):
    def test_form_relationship_exist(self):
        user=CustomUser.objects.create_user(email="test@gmail.com",password="test1234#",name="test",Phone="123456789")
        data={'Name':"test" ,'Phone':'1234567889','Pincode':'123456','State':'test','house_no':'dff','Road_name':"sd"}
        form=address_form(data=data)
        self.assertTrue(form.is_valid())

class otp_test(TestCase):
    def test_otp_form(self):
        data={'otp_digit':'lenghtmorethan6'}
        form=otp_form(data=data)
        self.assertFalse(form.is_valid())
        





        
    

        

