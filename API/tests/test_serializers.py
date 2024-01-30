from rest_framework.test import APITestCase
from API.serializers import User_serializer
from User_Account.models import CustomUser


class test_User_serializer(APITestCase):
    # Test to check if create and is_valid of User_serializer is working properly
    def test_user_register(self):
        data={
            "email":"test@gmail.com",
            "name":"test",
            "Phone":"127845469",
            "password1":"t1234est#",
            "password2":"t1234est#"
        }

        serializer=User_serializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertTrue(CustomUser.objects.filter(email=data["email"]).exists())


    # Test to check validation error if password fields does'nt match
    def test_user_register_validation_error(self):
        data={
            "email":"test@gmail.com",
            "name":"test",
            "Phone":"127845469",
            "password1":"t1234est#",
            "password2":"passwordchanged"
        }

        serializer=User_serializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue(serializer.errors)
        self.assertIn("Password and Confirm_Password doesn't match.", serializer.errors['non_field_errors'])

        


        


