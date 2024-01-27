from rest_framework import serializers
from User_Account.models import CustomUser,user_address


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
    

    def create(self, validated_data):
        user = CustomUser.objects.create_user(email=validated_data['email'],password=validated_data['password1'],name=validated_data['name'],Phone=validated_data['Phone'])
        user.save()
        user.is_active=False
        user.save()
        return user
    

class LoginSerializers(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    password=serializers.CharField(style={'input_type':'password'})


class User_ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name','Phone']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.Phone = validated_data.get('Phone', instance.Phone)
        instance.save()
        return instance
    

class User_AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_address
        fields = ['Name','Phone','Pincode','State','house_no','Road_name']


class PasswordChangeSerializer(serializers.Serializer):
    old_password=serializers.CharField(style={'input_type':'password'})
    new_password1=serializers.CharField(style={'input_type':'password'})
    new_password2=serializers.CharField(style={'input_type':'password'})


    def validate(self, attrs):
        new_password1 = attrs.get('new_password1')
        new_password2 = attrs.get('new_password2')

        if new_password1 != new_password2:
            raise serializers.ValidationError("Password and Confirm_Password doesn't match.")
        return attrs
