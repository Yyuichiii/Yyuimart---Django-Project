from django.test import TestCase
from User_Account.models import CustomUser,user_address,User_cart,Order
from django.core.exceptions import ValidationError


class User_check_test(TestCase):
    def test_createuser(self):
        user=CustomUser.objects.create_user(email="test@gmail.com",password="test",name="test",Phone="123456789")
        self.assertEqual(user.email,"test@gmail.com")
        self.assertEqual(user.name,"test")
        self.assertEqual(user.Phone,"123456789")
        self.assertTrue(user.check_password("test"))

    # This error when ValueError exists 
    # def test_email_not_set(self):
    #     with self.assertRaises(ValueError) as context:
    #         user=CustomUser.objects.create_user(email="",password="test",name="test",Phone="123456789")
    #     self.assertEqual(str(context.exception), "The Email must be set")
        
    def test_superuser(self):
        user=CustomUser.objects.create_superuser(email="test@gamil.com",password="test")
        self.assertEqual(user.email,"test@gamil.com")
        self.assertTrue(user.check_password("test"))
        self.assertTrue(user.is_staff)
        self.assertEqual(user.name,"Admin")
        self.assertEqual(str(user),"test@gamil.com")
        self.assertEqual(user.__str__(),"test@gamil.com")
        self.assertEqual(user.get_full_name(),"")


    def test_email_validations(self):
        obj=CustomUser(email="invalidEMail",password="test",name="test",Phone="123456789")
        
        with self.assertRaises(ValidationError) as context:
            obj.full_clean()
        # print(context.exception.message_dict)
        self.assertEqual(context.exception.message_dict['email'][0],'Enter a valid email address.')
    
    
    def test_Phone_validations(self):
        obj=CustomUser(email="test@gmail.com",password="test",name="test",Phone="invalidPhone")
        
        with self.assertRaises(ValidationError) as context:
            obj.full_clean()
        self.assertEqual(context.exception.message_dict['Phone'][0],'Enter a valid Phone number.')

        obj=CustomUser(email="test@gmail.com",password="test",name="test",Phone="")
        with self.assertRaises(ValidationError) as context:
            obj.full_clean()
        self.assertEqual(context.exception.message_dict['Phone'][0],'This field cannot be blank.')


class User_Address_test(TestCase):
    # test the one to one relation between CustomUser model and user_address model
    def test_relation(self):
        user=CustomUser.objects.create_user(email="test@gmail.com",password="test",name="test",Phone="123456789")
        address_obj=user_address.objects.create(user=user,Name="test",Phone="test",Pincode="test",State="test",house_no="test",Road_name="test")
        self.assertEqual(address_obj.user,user)

    def test_user_address_validations(self):
        user=CustomUser.objects.create_user(email="test@gmail.com",password="test",name="test",Phone="123456789")

        # Creates a model only with user,Name,Phone fields to raise a ValidationError
        obj2=user_address(user=user,Name="test",Phone="122435")
        with self.assertRaises(ValidationError) as context:
            obj2.full_clean()

        self.assertEqual(context.exception.message_dict['Pincode'][0],"This field cannot be blank.")
        self.assertEqual(context.exception.message_dict['State'][0],"This field cannot be blank.")
        self.assertEqual(context.exception.message_dict['house_no'][0],"This field cannot be blank.")
        self.assertEqual(context.exception.message_dict['Road_name'][0],"This field cannot be blank.")
        

class User_cartt(TestCase):
    def test_validatators(self):
        user=CustomUser.objects.create_user(email="test@gmail.com",password="test",name="test",Phone="123456789")

        # model with PIamge field not provided
        cart=User_cart(user=user,PID="test",Category="test",Brand="test",PName="test",Price=12,Quantity=2)

        with self.assertRaises(ValidationError) as context:
            cart.full_clean()
        self.assertTrue(context.exception.message_dict['PImage'][0],'This field cannot be blank.')


        



    