from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
import pyotp
import qrcode
import io
import base64

from .models import User, StudentProfile, LecturerProfile, LoginHistory, BlockedUser, StudentLeaderProfile, ClassRepProfile
from .serializers import (
    RegisterSerializer, CustomTokenObtainPairSerializer, UserSerializer,
    StudentProfileSerializer, LecturerProfileSerializer, ChangePasswordSerializer,
    OTPVerifySerializer, ForgotPasswordSerializer, ResetPasswordSerializer,
    TwoFactorSetupSerializer, LoginHistorySerializer, BlockedUserSerializer,
    StudentLeaderProfileSerializer, ClassRepProfileSerializer
)
from .permissions import IsOwnerOrAdmin, IsStudentLeader, IsClassRep


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Registration successful.'}, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            try:
                user = User.objects.get(email=request.data.get('email'))
                LoginHistory.objects.create(
                    user=user,
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    success=True
                )
                user.last_login_ip = get_client_ip(request)
                user.save(update_fields=['last_login_ip'])
            except Exception:
                pass  # Never let login history crash the login response
        return response


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully.'})
        except Exception:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(email=data['email'])
            otp = OTPVerification.objects.filter(
                user=user, code=data['code'], purpose='email_verify', is_used=False
            ).latest('created_at')
            if not otp.is_valid():
                return Response({'error': 'OTP expired.'}, status=status.HTTP_400_BAD_REQUEST)
            otp.is_used = True
            otp.save()
            user.is_verified = True
            user.is_active = True
            user.save(update_fields=['is_verified', 'is_active'])
            return Response({'message': 'Email verified successfully.'})
        except (User.DoesNotExist, OTPVerification.DoesNotExist):
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)


class ResendOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        return Response({'message': 'OTP sent.'})


class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        return Response({'message': 'If the email exists, a reset code has been sent.'})


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(email=data['email'])
            otp = OTPVerification.objects.filter(
                user=user, code=data['code'], purpose='password_reset', is_used=False
            ).latest('created_at')
            if not otp.is_valid():
                return Response({'error': 'OTP expired.'}, status=status.HTTP_400_BAD_REQUEST)
            otp.is_used = True
            otp.save()
            user.set_password(data['new_password'])
            user.save()
            return Response({'message': 'Password reset successful.'})
        except (User.DoesNotExist, OTPVerification.DoesNotExist):
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'message': 'Password changed successfully.'})


class TwoFactorSetupView(APIView):
    def get(self, request):
        user = request.user
        if not user.two_factor_secret:
            user.two_factor_secret = pyotp.random_base32()
            user.save(update_fields=['two_factor_secret'])
        totp = pyotp.TOTP(user.two_factor_secret)
        uri = totp.provisioning_uri(name=user.email, issuer_name='CampusConnect')
        img = qrcode.make(uri)
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        qr_b64 = base64.b64encode(buffer.getvalue()).decode()
        return Response({'qr_code': f'data:image/png;base64,{qr_b64}', 'secret': user.two_factor_secret})

    def post(self, request):
        serializer = TwoFactorSetupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        totp = pyotp.TOTP(user.two_factor_secret)
        if totp.verify(serializer.validated_data['code']):
            user.two_factor_enabled = True
            user.save(update_fields=['two_factor_enabled'])
            return Response({'message': '2FA enabled successfully.'})
        return Response({'error': 'Invalid code.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.two_factor_enabled = False
        user.two_factor_secret = ''
        user.save(update_fields=['two_factor_enabled', 'two_factor_secret'])
        return Response({'message': '2FA disabled.'})


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class StudentProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentProfileSerializer

    def get_object(self):
        profile, _ = StudentProfile.objects.get_or_create(user=self.request.user)
        return profile


class LecturerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = LecturerProfileSerializer

    def get_object(self):
        profile, _ = LecturerProfile.objects.get_or_create(user=self.request.user)
        return profile


class LoginHistoryView(generics.ListAPIView):
    serializer_class = LoginHistorySerializer

    def get_queryset(self):
        return LoginHistory.objects.filter(user=self.request.user)


class BlockUserView(APIView):
    def post(self, request, user_id):
        try:
            blocked_user = User.objects.get(id=user_id)
            if blocked_user == request.user:
                return Response({'error': 'Cannot block yourself.'}, status=status.HTTP_400_BAD_REQUEST)
            BlockedUser.objects.get_or_create(blocker=request.user, blocked=blocked_user)
            return Response({'message': 'User blocked.'})
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id):
        BlockedUser.objects.filter(blocker=request.user, blocked_id=user_id).delete()
        return Response({'message': 'User unblocked.'})


class BlockedUsersListView(generics.ListAPIView):
    serializer_class = BlockedUserSerializer

    def get_queryset(self):
        return BlockedUser.objects.filter(blocker=self.request.user)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    filterset_fields = ['role', 'is_active', 'is_verified']
    search_fields = ['email', 'first_name', 'last_name']


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()


class StudentLeaderProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentLeaderProfileSerializer

    def get_object(self):
        profile, _ = StudentLeaderProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get_permissions(self):
        return [IsStudentLeader()]


class StudentLeaderListView(generics.ListAPIView):
    serializer_class = StudentLeaderProfileSerializer
    filter_backends = [__import__('django_filters.rest_framework', fromlist=['DjangoFilterBackend']).DjangoFilterBackend]
    filterset_fields = ['university', 'is_active']

    def get_queryset(self):
        return StudentLeaderProfile.objects.filter(is_active=True)


class ClassRepProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ClassRepProfileSerializer

    def get_object(self):
        profile, _ = ClassRepProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get_permissions(self):
        return [IsClassRep()]
