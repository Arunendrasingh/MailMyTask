from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import CustomUser

# Your Serializer


class RegisterUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name",
                  "contact", "password", "password1"]
        extra_kwargs = {
            'email': {'validators': [UniqueValidator(queryset=CustomUser.objects.all())]},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': True, "write_only": True},
            'contact': {'required': True, 'validators': [UniqueValidator(queryset=CustomUser.objects.all())]},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs["password1"]:
            raise serializers.ValidationError(
                {"password": "password field did't match."})
        return super().validate(attrs)

    def create(self, validated_data):
        user: CustomUser = CustomUser.objects.create_user(
            validated_data['email'], validated_data['contact'], validated_data['password'])
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.save()
        return user
