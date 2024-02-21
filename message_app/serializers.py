from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.fields import CurrentUserDefault
from .models import Message
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    """Serialize user class"""
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=128, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        read_only_fields = ('id',)


    def create(self, validated_data):
        """Create and validate a user"""
        try:
            validate_password(validated_data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})

        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class MessageSerializer(serializers.ModelSerializer):
    message_from = serializers.CharField(read_only=True, default=CurrentUserDefault())
    message_to = serializers.CharField()
    message_title = serializers.CharField(max_length=100)
    message_content = serializers.CharField(max_length=255)

    viewed_at = serializers.DateTimeField(read_only=True)
    is_viewed = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'message_from', 'message_to', 'message_title', 'message_content',  'created_at', 'is_viewed', 'viewed_at')#, 'is_viewed', 'viewed_at')
        read_only_fields = ('id',)
