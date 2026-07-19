from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input':'password'})
    class Meta :
        model = User
        fields = ['email', 'username','password']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise serializers.ValidationError('user does not exist!, Sign up first!')
            if not user.is_active:
                raise serializers.ValidationError('user is blacklisted or deactivated!')
        else:
            raise serializers.ValidationError('password and email field is required!')
        
        attrs['user'] = user
        return attrs