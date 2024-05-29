from rest_framework import serializers
from .models import User

class RegisterSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'password', 'first_name', 'last_name')

class VerifyPhoneSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)

class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone', 'first_name', 'last_name', 'email', 'user_roll')

class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)

class ResetPasswordVerifySerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)

class UpdateUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'notification', 'auto_brightness',
                  'birthday', 'gender', 'language', 'married', 'status', 'city',
                  'children', 'animal', 'car')

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('notification', 'auto_brightness')

class DeleteAccountSerializer(serializers.Serializer):
    pass  # If needed, you can add fields for additional verification

class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
