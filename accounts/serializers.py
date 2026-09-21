from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from datetime import timedelta
import random
import pyotp
from .models import User, StudentProfile, LecturerProfile, OTPVerification, LoginHistory, BlockedUser, StudentLeaderProfile, ClassRepProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        self._send_verification_otp(user)
        return user

    def _send_verification_otp(self, user):
        from .tasks import send_otp_email
        code = str(random.randint(100000, 999999))
        OTPVerification.objects.create(
            user=user,
            code=code,
            purpose='email_verify',
            expires_at=timezone.now() + timedelta(minutes=10)
        )
        try:
            send_otp_email.delay(user.email, code, 'email_verify')
        except Exception:
            send_otp_email(user.email, code, 'email_verify')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['full_name'] = user.full_name
        token['is_verified'] = user.is_verified
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        data['full_name'] = self.user.full_name
        data['two_factor_enabled'] = self.user.two_factor_enabled
        return data


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'full_name', 'role',
                  'is_active', 'is_verified', 'two_factor_enabled', 'date_joined')
        read_only_fields = ('id', 'date_joined', 'is_verified', 'is_active')


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = '__all__'
        read_only_fields = ('user',)


class LecturerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = LecturerProfile
        fields = '__all__'
        read_only_fields = ('user',)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    purpose = serializers.ChoiceField(choices=['email_verify', 'password_reset', 'two_factor'])


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(validators=[validate_password])


class TwoFactorSetupSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)


class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistory
        fields = '__all__'


class BlockedUserSerializer(serializers.ModelSerializer):
    blocked = UserSerializer(read_only=True)

    class Meta:
        model = BlockedUser
        fields = ('id', 'blocked', 'created_at')


class StudentLeaderProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentLeaderProfile
        fields = '__all__'
        read_only_fields = ('user',)


class ClassRepProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ClassRepProfile
        fields = '__all__'
        read_only_fields = ('user',)
