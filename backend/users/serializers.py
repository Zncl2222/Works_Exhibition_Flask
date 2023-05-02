from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class EmailValidationSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EmailTokenValidationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=64)
