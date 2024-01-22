from rest_framework import serializers
from User_Account.models import CustomUser


class User_serializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['name','email','Phone','password1','password2']
        

    def validate(self, attrs):
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')

        if password1 != password2:
            raise serializers.ValidationError("Password and Confirm_Password doesn't match.")
        return attrs
    
    def validate_email(self,email):
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('user with this Email already exists.')
        return email

    def create(self, validated_data):
        user = CustomUser.objects.create_user(email=validated_data['email'],password=validated_data['password1'],name=validated_data['name'],Phone=validated_data['Phone'])
        user.save()
        user.is_active=False
        user.save()
        return user