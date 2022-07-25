import email
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","first_name","last_name","email","password"]

    def create(self, validated_data):
        if User.objects.filter(username=validated_data["username"]).exists():
            return 
        else:
            return User.objects.create(
                username = validated_data['username'],
                first_name = validated_data['first_name'],
                last_name = validated_data['last_name'],
                email = validated_data['email'],
                password = validated_data['password']
            )

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=40)
    password = serializers.CharField(max_length=40)

    def validate(self, attrs):
        if attrs['username'] != "":
            if len(attrs['password']) >= 1:
                return attrs
            else:
                raise serializers.ValidationError("Length of password must be greater than 8")
        else:
            raise serializers.ValidationError(["Something went wrong"])
            
            

    