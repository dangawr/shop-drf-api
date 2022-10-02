from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        write_only=True, style={'input_type': 'password'}
    )

    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValueError('Passwords must be the same!')
        else:
            del attrs['password2']
            return attrs

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)



